# TITLE: TRYpros Python Package
# Contributors: Gayathri Girish Nair (girishng@tcd.ie)

# INFER VERSION
try:
    from importlib.metadata import version
    __version__ = version("TRYpros")
except ImportError:
    __version__ = "unknown"

# IMPORTS
import copy
import datetime
import calendar
import numpy as np
import pandas as pd
import global_land_mask
import cartopy.crs as ccrs
from pyproj import Transformer
import matplotlib.pyplot as plt

# CONSTANTS
_MONTHS = [v.lower() for v in list(calendar.month_name) if len(v) > 0]
_MONTHS_SHORT = [v[:3] for v in _MONTHS]
_SEASONS = ["summer", "autumn", "winter", "spring", 'fall']
_CONTEXT_COLS = ["DataName", "OriglName", "OrigUnitStr", "Comment"]
_VALID_DATA_TYPES = ["trait", "lonlat", "year"]
_VALID_STD_TYPES = ["std", "non_std"]

# HELPER FUNCTIONS
def _is_float(s):
    """ Checks if this string is that of a float or not.
    
    Keyword Arguments:
    s {str} -- String value.

    Returns:
    {bool} -- Whether this is a float string.
    """
    try: float(s)
    except: return False
    return True

def _replace_month(val, with_m:bool):
    """ Replaces the month substring in the given string.

    val {str|nan} -- The string containing the month.
    with_m {bool} -- If True, the month substring is replaced with 'm'
                     else it gets replaced with the short representation
                     of the month.
    
    Returns:
    val {str|nan} -- Date string with month substring replaced.
    """
    # If date_str is not a "str" object then the same
    # value is returned without any processing.
    if val == val and type(val) == str:
        val = val.lower()
        for m in _MONTHS:
            m_short = m[:3]
            val = val.replace(m, m_short)
        if with_m:
            for m in _MONTHS_SHORT: 
                val = val.replace(m, "m")
    return val

def _replace_season(val):
    """ Replaces any season name substrings in the given string with "s".
    
    Keyword Arguments:
    val {str|nan} -- The string containing the month.

    Returns:
    val {str|nan} -- String with the season name replaced by "s".
    """
    if val == val and type(val) == str: 
        val = val.lower()
        for s in _SEASONS:
            val = val.replace(s, "s")
    return val

def _get_form(val, num_placeholder='@', rep_month=True, 
              rep_season=True, make_lower=True):
    """ Gets general form of value with numbers replaced with '@'.
    
    Keyword Arguments:
    val {any} -- Value, the form of which, is to be returned.
    num_placeholder {str} -- The symbol that should replace 
                            numbers (Default '@').
    rep_month {bool} -- Whether or not to replace month substrings
                        in the val with character 'm'. (Default True)
    rep_season {bool} -- Whether or not to replace season substrings
                         in the val with character 's'. (Default True)
    make_lower {bool} -- Whether or not to make form all lowercase.
                         (Default True)
    
    Returns:
    val_form {str} -- General form of the given value.
    """
    # If value is NaN, return NaN.
    if val != val: return val
    val_str = str(val) if type(val) != str else val
    val_form = ""
    is_num = False
    num_points = 0
    for i in range(len(val_str)):
        c = val_str[i]
        if c.isnumeric():  # Character is a number.
            if not is_num:  # Previous character was not a number.
                is_num = True
                val_form += num_placeholder
        else:  # Character is not a number.
            if (c == "."):  # Character is a point.
                num_points += 1
            if not(
                c == 1 and  # This is the first point encountered
                is_num and  # since the previous character was a number.
                i + 1 < len(val_str) and  # There is a next character
                val_str[i+1].isnumeric()  # such that is is also a number.
            ):  # The above is not the case.
                is_num = False
                num_points = 0
                val_form += c
    if rep_month: 
        val_form = _replace_month(val_form, with_m=True)
    if rep_season: 
        val_form = _replace_season(val_form)
    if make_lower: 
        val_form = val_form.lower()
    val_form = val_form.strip()
    return val_form

def _get_covariate_matches(df, search_str_list, print_matches):
    """  Returns DataIDs of matched covariates.

    Returns DataIDs of covariates whose names are matched
    with given search strings. Search characteristics
    involves an AND operation between words in each term and
    an OR operation between the terms themselves.

    Keyword Arguments:
    df {pd.DataFrame} -- Pandas data frame with data from TRY containing
                         columns "DataID" and "DataName".
    search_str_list {list} -- List of search strings.
    print_matches {bool} -- Whether or not matches are to be 
                            printed out.
    
    Returns:
    {list} -- List of DataIDs.
    """
    df_subset = df[["DataID", "DataName"]].dropna().drop_duplicates()
    ids = set([])
    for data_id, data_name in df_subset.values:
        name = str.lower(data_name)
        for search_str in search_str_list:
            all_words_present = True # All words in the same search term.
            for word in search_str.split():
                all_words_present &= (word in name)
            if all_words_present: ids.add(data_id)
    if print_matches:
        for data_id, data_name in df_subset[
            df_subset.DataID.isin(ids)].values:
            print(f"({data_id}) {data_name}")
    return list(ids)

def _wgs84_m_utm_to_decimal_degrees(easting, northing, zone, hemisphere):
    """ Converts UTM values to decimal degrees.
    
    Converts X and Y values expressed in meters with the 
    coordinate reference system being UTM and  
    WGS84 reference datum to latitude and longitude values
    expressed in decimal degrees ([-180, 180], [-90, 90]).

    Keyword Arguments:
    easting {float} -- Longitude equivalent.
    northing {float} -- Latitude equivalent.
    zone {int} -- UTM Zone.
    hemisphere {str} -- Vertical geographic hemisphere (N/S).

    Returns:
    {pd.Series} -- Longitude and latitude.
    """
    latitude = np.nan
    longitude = np.nan
    if(
        easting == easting and 
        northing == northing and 
        zone == zone and 
        hemisphere == hemisphere
    ):
        # Build the UTM CRS string
        utm_crs = f"EPSG:326{zone}" if hemisphere == 'n' else f"EPSG:327{zone}"
        # Define the transformer (UTM to WGS84)
        transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True) 
        # Convert to decimal degrees (longitude, latitude)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([longitude, latitude])

def _nztm_to_decimal_degrees(easting, northing):
    """ Converts NZTM to decimal degrees.
    
    Converts New Zealand Transverse Mercator (NZTM) 
    coordinates to decimal degrees ([-180, 180], [-90, 90]).
    
    Keyword Arguments:
    easting {float} -- Longitude equivalent.
    northing {float} -- Latitude equivalent.
    
    Returns:
    {pandas.Series} -- Longitude and latitude in decimal degrees.
    """
    latitude = np.nan
    longitude = np.nan
    if(easting == easting and northing == northing): # If not NaN.
        transformer = Transformer.from_crs(
            "EPSG:2193", # NZTM 
            "EPSG:4326", # WGS84 (decimal degrees)
            always_xy=True)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([longitude, latitude])

def _value_std_latlon_deg(r):
    """ Converts non-standard decimal degrees into standard format.
    
    Given a longitude or latitude value expressed in
    degrees using one of many styles in the TRY DB,
    this function converts that style into the standard
    decimal degree format, which is a float value in
    the range -180 to 180 for longitude values and
    -90 to 90 for latitude values. Only those rows where
    OrigUnitStr == "decimal degrees" will be considered here.
    """
    value = r.OrigValueStr
    if value == value: # Not NaN
        value = str(value).lower()
        form = str(r.value_form).lower()
        unit = str(r.OrigUnitStr)

        # UTM values will be processed later by the 
        # value_transformation_latlon(...) function.
        # So for now, return UTM related values, as is.
        if unit == "decimal degrees": 
            # Standard formats.
            if form in ["@", "-@", "@.@", "-@.@"]: 
                return float(value)
    
            # Non Standard formats.
            # Standardize form's form.
            form = form.replace("n", "D")
            form = form.replace("e", "D")
            form = form.replace("w", "D")
            form = form.replace("deg", "d ")
            form = form.replace('sec', '"')
            form = form.replace("s", "D")
            form = form.replace("°", "d ")
            form = form.replace("''", "s ")
            form = form.replace("'", "m ")
            form = form.replace("´", "m ")
            form = form.replace('"', "s ")
            # Standardize value's form.
            value = value.replace("deg", "d")
            value = value.replace('sec', 's ')
            value = value.replace("°", "d ")
            value = value.replace("''", "s ")
            value = value.replace("'", "m ")
            value = value.replace("´", "m ")
            value = value.replace('"', "s ")

        # Proceed only if cardinal direction is available.
        if "D" in form:
            # Extract hemisphere, degrees, minutes, seconds.
            hemisphere = 1 # ["N", "E"]
            degrees = 0
            minutes = 0
            seconds = 0
            if str.upper(value[-1]) in ["S", "W"]: 
                hemisphere = -1
            value_split = [
                v.strip() for v in value.split(" ") 
                if v != " " and len(v.strip()) > 0
            ]
            for i in range(len(value_split)):
                v = value_split[i]
                if i == 0: # First value should always be degree.
                    v = v.replace("d", "")
                    if _is_float(v):
                        degrees = float(v)
                    else: return np.nan
                else:
                    if "m" in v: # Value is minutes
                        v = v.replace("m", "")
                        if _is_float(v):
                            minutes = float(v)
                    elif "s" in v:
                        v = v.replace("s", "")
                        if _is_float(v):
                            minutes = float(v)
            decimal_degrees = hemisphere * (
                degrees + (minutes / 60) + (seconds / 3600))
            return decimal_degrees
    return value

def _extract_year(date_str):
    """ Extracts year from given date string.

    Keyword Arguments:
    date_str {str} -- A string representation of date.
    
    Returns:
    {int} -- Year if the date form is a single matched date, 
             mean year if it is a date range date range, or NaN otherwise.
    """
    current_year = datetime.date.today().year

    if date_str == date_str: # No NaN.
        date_str = str(date_str)
        date_str = date_str.replace("(", "")
        date_str = date_str.replace(")", "")
        date_str = date_str.replace(",", "-")
        date_str = date_str.replace("/", "-")
        date_str = date_str.replace("&", "-")
        date_str = date_str.replace(".", "-")
        date_str = date_str.replace("t", "-")
        date_str = date_str.replace("?", "")
        date_str = date_str.replace(" ", "-")

        date_split = date_str.split("-")

        years = np.sort([
            y.strip() for y in date_split 
            if y.strip().isnumeric() and len(y.strip()) == 4
        ]).tolist()
        
        # If more than 1 year found, compute average.
        if len(years) > 0:
            year_start = int(years[0])
            year_end = int(years[-1])
            if (year_start <= current_year 
                and year_end <= current_year): # No future years.
                year_final = str(int(np.ceil((year_start + year_end) / 2)))
                return year_final
            
    # Any other situation is considered invalid. 
    return np.nan 

def _validate_data_type(data_type):
    """ Raises exception if data_type is invalid.

    Keyword Arguments:
    data_type {str} -- String to check if valid.
    """
    global _VALID_DATA_TYPES
    if not data_type in _VALID_DATA_TYPES:
        raise Exception("Invalid data_type. "
                        + f"Expected one of {_VALID_DATA_TYPES}.")
    
def _validate_std_type(std_type):
    """ Raises exception if std_type is invalid.

    Keyword Arguments:
    std_type {str} -- String to check if valid.
    """
    global _VALID_STD_TYPES
    if not std_type in _VALID_STD_TYPES:
        raise Exception("Invalid std_type. "
                        + f"Expected one of {_VALID_STD_TYPES}.")

# MAIN
class DFColValTransformation:
    "Data Frame Column Value Transformation"

    def __init__(self, f, col, name=None):
        """ Constructor.

        Keyword Arguments:
        name {str} -- Transformation name. Will be same as
                      name of the 'f' function if None.
                      (Default None)
        f {function} -- Function that is to be applied.
                        This function should look as follows:
                        def my_function(row):
                            ''' Transform given value. 
                            
                            Keyword Arguments:
                            row {pd.Series} -- Row of dataset containing
                                               the column with the value
                                               to be transformed.

                            Returns:
                            v {type of value in column 'col'} 
                                -- Transformed column value in given row.
                            '''
                            ...
                            return v
        col {str} -- Name of the column containing values that will be
                     transformed.
        """
        self.name = f.__name__ if name is None else name
        self.desc = f.__doc__
        self.f = f
        self.col = col

    def __str__(self):
        """ String representation of this object. """
        f_str = self.name
        if self.desc is not None:
            f_str += f": {self.desc}"
        return f_str
    
    def __call__(self, df):
        """ Applies given function to the value per row of given column.

        The dataframe is deep copied before the transformation is
        applied to avoid in-place value mutation.

        Keyword Arguments:
        df {str} -- DataFrame whose values are to be transformed.

        Returns:
        df_t {pandas.DataFrame} -- DataFrame with column values replaced
                                   with transformed values.
        """
        if not self.col in df.columns:
            raise Exception("Given data frame does not contain "
                            + f"configured column '{self.col}'.")
        df_t = copy.deepcopy(df)
        df_t.loc[:, self.col] = df_t.apply(self.f, axis=1)
        return df_t

class FeatureHandler:
    """ Feature Handler. """

    def __init__(self, feature_name, d_type, path_src, path_ref):
        """ Constructor. 
        
        Keyword Arguments:
        feature_name {str} -- Name of this feature.
        d_type {str} -- Data type of value. Valid options include
                        ["float", "int", "str"]
        path_src {str} -- Path to location of .txt file containing
                          data as downloaded from the TRY Plant DB.
        path_ref {str} -- Path to a .txt file in which DatasetIDs
                          from loaded data shall be stored for
                          referencing later. New IDs shall be
                          appended to any IDs already in this file,
                          ensuring that there are no duplicates.
        """
        if not d_type in ["float", "int", "str"]:
            raise Exception(f"Invalid d_type = '{d_type}'.",
                            + f" Expected one of ['float', 'int', 'str']")
        self.feature_name = feature_name
        self.d_type = d_type
        self.path_src = path_src
        self.path_ref = path_ref
        self.data_raw = None
        self.data_trait = None
        self.data_covariate = None
        self.data_lonlat = None
        self.data_year = None

        # CONFIGURATIONS
        self.known_ids = {"trait": None, "year": None, "lonlat": None}
        self.keep_ids = {"trait": None, "year": None, "lonlat": None}
        self.options_value_form = {"replace_month": True,
                                   "replace_season": True,
                                   "make_lower": True}
        self.transforms = {
            "std": {"trait":[], "lonlat":[], "year":[]},
            "non_std": {"trait":[], "lonlat":[], "year":[]}}

    # HELPER FUNCTIONS
    def _get_form(self, v):
        """ Returns form of values. 
        
        Keyword Arguments:
        v {any} -- Value to get form of.
        """
        return _get_form(
            val=v, rep_month=self.options_value_form["replace_month"],
            rep_season=self.options_value_form["replace_season"],
            make_lower=self.options_value_form["make_lower"])

    # DIAGNOSTICS FUNCTIONS
    def get_chunk_count(self, chunk_size):
        """ Gets no. of chunks of data if each chunk is the given size.
        
        Returns no. of chunks that the data will be divided
        into if, chunk size for data loading is a certain value.
        
        Keyword Parameters:
        chunk_size {int} -- Chunk size (integer).

        Returns:
        num_chunks {int} -- The no. of chunks.
        """
        # Load downloaded data from TRY.
        num_chunks = 0
        for _ in pd.read_csv(self.path_src, delimiter = "\t",
                             encoding = "ISO-8859-1",
                             chunksize = chunk_size,
                             low_memory = False): num_chunks += 1
        return num_chunks
    
    def view_units_value_forms(self, data_type):
        """ Displays unit and value forms of std & non-std data.
        
        Displays some key information about pre-standardized
        and non-standardized values like their units and value forms.
        This function is expected to be useful data exploration.
        
        Keyword Arguments:
        data_type {str} -- The type of data from which units and
                           forms are to be extracted. This may be 
                           "trait", "latlon", or "year".
        """
        _validate_data_type(data_type)
        data = self.data_trait # data_type == "trait"
        if data_type == "lonlat": data = self.data_lonlat
        elif data_type == "year": data = self.data_year
        if data is None:
            print(f"No '{data_type}' data.",
                  f"Attribute data_{data_type} = None.")
        else:
            labels = [data_type[0].upper() + data_type[1:]]
            if data_type == "lonlat":
                data = [data["lon"], data["lat"]]
                labels = [labels[0] + " Longitude",
                          labels[0] + " Latitude"]
            else: data = [data]
            for d, l in zip(data, labels):
                # View units.
                std_units = d["std"].UnitName.dropna().unique().tolist()
                non_std_units = d[
                    "non_std"].OrigUnitStr.dropna().unique().tolist()
                print(f"{l} Standardised Units:", std_units)
                print(f"{l} Non-Standardised Units:", non_std_units)
                # View value forms.
                std_value_forms = d["std"].value_form.unique().tolist()
                non_std_value_forms = d[
                    "non_std"].value_form.unique().tolist()
                print(f"{l} Standardised Value Forms:", std_value_forms)
                print(f"{l} Non-Standardised Value Forms:",
                    non_std_value_forms)
            
    def get_context(self, data, context_cols=None):
        """ Displays unique value combinations of contextual columns.

        Keyword Arguments:
        data {pd.DataFrame} -- Data to view contextual columns of.
        return_view {bool} -- Whether or not to return data frame view.
                              (Default False)
        pd_display {bool} -- If True, displays the data using the 
                             'display()' function in pandas. If false,
                              the normal 'print()' function is used. If
                              you are running this in a notebook, then 
                              it is recommended to set this parameter to
                              True. (Default False)
        context_cols {list} -- List of columns names that should be present
                               in returned data frame. If None, then 
                               context columns is assumed to be 'DataName', 
                               'OriglName', 'OrigUnitStr', 'Comment'
                               key_try_cols["context"] is used instead.

        Returns:
        data_view {pandas.DataFrame} -- Pandas dataframe with unique rows
                                        of selected columns.
        """
        if context_cols is None:
            context_cols = _CONTEXT_COLS
        data_view = data[context_cols].drop_duplicates()
        return data_view

    def get_unique_matches(self, data, match_col, to_match, keep=[]):
        """ Get unique rows that match given column values.

        Given a data frame with returns unique rows that correspond
        to values in a given column that matches a given value list.

        Keyword Arguments:
        data {pandas.DataFrame} -- Data frame with 'value_form' column.
        match_col {str} -- Column to search for matches within.
        to_match {list} -- List of values to match.
        keep {list} --  List of columns to return. The default
                        value of [] implies that all columns shall be
                        returned. (Default [])
        
        Returns:
        data_view: Data frame subset containing all 
                   unique rows with matching value forms.
        """
        if not match_col in data.columns:
            raise Exception("Given DataFrame contains "
                            + "no 'value_form' column.")
        data_view = data[data[match_col].isin(to_match)]
        if len(keep) > 0: data_view = data_view.loc[:, keep]
        data_view = data_view.drop_duplicates()
        return data_view

    def get_combine_lonlat(self, std_type):
        """ Combines longitude and latitude data for easier exploration.

        Keyword Arguments.
        std_type {str} -- Type of standardization. Valid options
                          include ["std", "non_std"].

        Returns:
        df_lonlat {pandas.DataFrame} -- Non standardized longitude
                                        and latitude data.
        """
        _validate_std_type(std_type)
        df_lonlat = pd.concat([self.data_lonlat["lon"][std_type],
                               self.data_lonlat["lat"][std_type]])
        df_lonlat = df_lonlat.drop_duplicates()
        df_lonlat = df_lonlat.reset_index(drop=True)
        return df_lonlat

    def get_utm_data(self, include_wgs=True):
        """ Gets rows corresponding to non-std lon lat data in UTM format.
        
        Keyword Arguments:
        include_wgs {bool} -- Whether or not to also match rows 
                              with WGS data. (Default True)
        
        Returns:
        {pd.DataFrame} -- Matched data subset.
        """
        df_lonlat = self.get_combine_lonlat("non_std")
        data_names = df_lonlat.DataName.astype(str).str.lower()
        original_names = df_lonlat.OriglName.astype(str).str.lower()
        comments = df_lonlat.Comment.astype(str).str.lower()

        # Extract UTM data.
        data_utm = df_lonlat[
            data_names.str.contains("utm")
            | original_names.str.lower().str.contains("utm")
            | comments.str.lower().str.contains("utm")]
        
        # Optionally extract WGS data.
        if include_wgs:
            data_wgs = df_lonlat[
                data_names.str.contains("wgs")
                | original_names.str.lower().str.contains("wgs")
                | comments.str.lower().str.contains("wgs")]
            data_utm = pd.concat([data_utm, data_wgs])
        
        data_utm = data_utm.drop_duplicates().reset_index(drop=True)
        return data_utm

    def get_nztm_data(self):
        """ Gets rows corresponding to non-std lon lat data in NZTM form.
        
        Returns:
        data_nztm: Matched data subset.
        """
        df_lonlat = self.get_combine_lonlat("non_std")
        data_names = df_lonlat.DataName.astype(str).str.lower()
        original_names = df_lonlat.OriglName.astype(str).str.lower()
        comments = df_lonlat.Comment.astype(str).str.lower()

        # Extract NZTM data.
        data_nztm = df_lonlat[
            data_names.str.contains("northtm")
            | original_names.str.lower().str.contains("easttm")
            | comments.str.lower().str.contains(
                "newzealandtransversemercator")]
        
        data_nztm = data_nztm.drop_duplicates().reset_index(drop=True)
        return data_nztm

    def get_feature_unit(self):
        """ Gets unit from current version of standardized trait data.
        
        Returns:
        feature_unit {str} -- Latest known standardized unit.
        """
        feature_unit = self.data_trait["std"].UnitName.dropna()
        if len(feature_unit) > 0: feature_unit = feature_unit.iloc[0]
        else: feature_unit = ""
        return feature_unit

    def get_considered_traits(self, data_type):
        """ Gets known traits currently configured to be kept. 
        
        Returns:
        data_keep {pandas.DataFrame} -- Subset of dataframe where 
                                        IDs match Trait/DataIDs to keep.
        """
        _validate_data_type(data_type)
        data_keep = self.known_ids[data_type]
        data_keep = data_keep[data_keep.id.isin(self.keep_ids[data_type])]
        return data_keep
    
    def view_range(self, data_type, std_type):
        """ Prints data range for given std type. 
        
        Keyword Arguments:
        data_type {str} -- Type of data. Valid options = ["trait",
                           "lonlat", "year"]
        std_type {str} -- Standardization type. Options include
                          ["std", "non_std"].
        """
        _validate_data_type(data_type)
        _validate_std_type(std_type)
        data_type_lbl = data_type[0].upper() + data_type[1:]
        std_type_lbl = "Std" if std_type == "std" else "Non Std"
        if data_type == "trait" and self.d_type != "float":
            raise Exception(
                "Cannot get min max values for non-numeric feature.")
        val_col = "StdValue" if std_type == "std" else "OrigValueStr"
        float_conv_successful = True
        if data_type == "lonlat":
            try:
                vals_lon = self.data_lonlat["lon"][std_type][
                    val_col].dropna().drop_duplicates().astype(float)
                vals_lat = self.data_lonlat["lat"][std_type][
                    val_col].dropna().drop_duplicates().astype(float)
            except Exception as e:
                float_conv_successful = False
                print("Could not extract float value from lonlat data.",
                      f"Exception: '{e}'")
            if float_conv_successful:
                print(f"{std_type_lbl} Longitude Value Range =",
                    vals_lon.describe().loc[
                        ["min", "max"]].to_numpy().tolist())
                print(f"{std_type_lbl} Latitude Value Range =",
                    vals_lat.describe().loc[
                        ["min", "max"]].to_numpy().tolist())
        else: # data_type in ["trait", "year"]
            vals = (self.data_trait if data_type == "trait" 
                    else self.data_year)[std_type][val_col]
            try:
                vals = vals.dropna().drop_duplicates().astype(float)
            except Exception as e:
                float_conv_successful = False
                print("Could not extract float value from lonlat data.",
                      f"Exception: '{e}'")
            if float_conv_successful:
                print(f"{std_type_lbl} {data_type_lbl} Value Range =",
                      vals.describe().loc[
                          ["min", "max"]].to_numpy().tolist())

    # DATA PROCESSING FUNCTIONS
    def load_big_data(self, drop_cols=[], chunk_size=10000, 
                      chunk_range=(-2, -1), clean=True):
        """ Loads a large data file. 
        
        This function sees to " it that NaN values in the StdValue 
        column are filled with values from the StdValueStr column 
        so that all standardized values, if available, may be found 
        in a single column "StdValue" instead of sometimes being 
        present under column "StdValueStr" instead of "StdValue". 
        Furthermore, this function extracts all unique TraitIDs within
        the data loaded. Loaded data and list of TraitIDs are stored
        in this object's data_raw and trait_id_list attributes.

        Keyword Arguments:
        drop_cols {list}: Columns to drop. Important columns for data
                          exploration ["TraitID", "DataID", "DatasetID",
                          "ObsDataID", "ObservationID", "AccSpeciesID", 
                          "StdValue", "StdValueStr", "UnitName",
                          "OrigValueStr", "OrigUnitStr", "OriglName",
                          "Comment"] WILL NOT be dropped even on request.
                          (Default [])
        chunk_size {int}: Data shall be loaded one chunk at a time to
                          minimize memory errors and kernel crashes. This
                          parameter defines the size of each data chunk.
                          (Default 10,000)
        chunk_range {int} -- A 2 element tuple wherein the first element
                             is the the index of the first data chunk to
                             load and the second element is the index of
                             the last data chunk that is to be loaded.
                             This parameter serves to allow loading of
                             only a portion of all data chunks when the
                             raw dataset is so large that it causes kernel
                             crashed even when loaded in chunks, if
                             attempting to load all the data in a single
                             processing session. (Default (-2, -1)
                             Indicates that all chunks are to be loaded.)
        clean {bool}: If True, performs the following two cleaning steps.
                      1. Drop duplicates.
                      2. Remove high risk error values.
                      (Default True) 

        Returns:
        data {pd.DataFrame}: Data as a pandas data frame.
        trait_id_list {list}: List of all trait ids found in the 
                              loaded data set.
        """
        print("LOADING BIG DATA:")
        print("Reading data ...", end=" ")
        # Load downloaded data from TRY.
        chunk_list = []

        i_start = chunk_range[0]
        i_end = chunk_range[1]
        step = 0 if i_start == -2 and i_end == -1 else 1
        i = -2 if step == 0 else 0
        for chunk in pd.read_csv(self.path_src, 
                                 delimiter = "\t",
                                 encoding = "ISO-8859-1", 
                                 chunksize = chunk_size,
                                 low_memory = False): 
            # Stop if ending chunk index is reached.
            if i == i_end: break
            # Consider only those chunks with the same index
            # as the start index or the index after the defined 
            # starting chunk index.
            if i >= i_start: chunk_list.append(chunk)
            i += step
        data = pd.concat(chunk_list, axis=0)
        print("done.")

        # Optionally clean dataset.
        if clean:
            print("Cleaning data ...", end=" ")
            # Drop duplicates.
            # The TRY 6.0 data release notes states that if a row contains 
            # an integer for the OrigObsDataID column, then this integer 
            # refers to the original obs_id of the observation that this
            # row is a duplicate of. Such duplicate records exist because
            # multiple studies can upload same data. Thus, keeping only those
            # records for which obs_id_of_original is NaN is equivalent to
            # dropping all duplicate observations in the dataset.
            data = data[data.OrigObsDataID.isna()]
            data.drop(["OrigObsDataID"], axis=1, inplace=True)

            # Risk minimization.
            # Also in TRY 6.0 data release notes, it is suggested that 
            # all records with Error Risk > 4 be dropped. 
            # Thus, this is done here as well.
            data.drop(data[data.ErrorRisk > 4].index, inplace=True)
            data.drop(["ErrorRisk"], axis=1, inplace=True)
            print("done.")

        print("Prepping data ...", end=" ")
        # Drop less useful columns.
        drop_cols += [col for col in drop_cols if not col in [ 
            # Ensure key columns are still retained.
            "TraitID", "DataID", "DatasetID", "ObsDataID",
            "ObservationID", "AccSpeciesID", "StdValue", 
            "StdValueStr", "UnitName", "OrigValueStr", 
            "OrigUnitStr", "OriglName", "Comment"
        ]] + ["Unnamed: 28"]
        data.drop(drop_cols, axis=1, inplace=True)

        # Fillna in StdValue column with value in StdValueStr column.
        data = data.assign(
            StdValue = data.StdValue.fillna(data.StdValueStr))
        print("done.")

        # Note down unique trait_ids found.
        print("Noting down unique TraitIDs ...", end=" ")
        df_trait = data[["TraitID", "TraitName"]]
        df_trait = df_trait.dropna(subset="TraitID")
        df_trait = df_trait.drop_duplicates()
        df_trait.columns = ["id", "name"]
        df_trait = df_trait.reset_index(drop=True)
        self.known_ids["trait"] = df_trait
        self.keep_ids["trait"] = df_trait.id.tolist()
        print("done.")

        # Save data into attributes.
        self.data_raw = data

        print("Noting down unique DatasetIDs for referencing later ...",
              end=" ")
        # Save dataset IDs for future referencing.
        dataset_ids = ""
        with open(self.path_ref, "r") as f:
            dataset_ids = set(f.read().split())
        for dataset_id in self.data_raw.DatasetID.unique():
            dataset_ids.add(str(dataset_id))
        with open(self.path_ref, "w") as f:
            f.write(" ".join(dataset_ids))
        print("done.")
        print("ALL DONE :3")

    def extract_trait_covariate_data(self, verbose=True):
        """ Extract trait data and separate it from covariate data.

        Only data associated with keep_ids is extracted. This function 
        also updates known lonlat and year DataIDs and assigns.
        Furthermore, this function separates trait and covariate
        data again based on whether it is standardized or not. A new
        column 'value_form' containing strings indicative of the general
        form of values is also added before storing trait and covariate
        data so obtained in attributes data_trait and data_covariate
        respectively.
        
        Keyword Arguments:
        verbose {bool} -- Whether or not to print possibly helpful
                          information about processed data.
                          (Default True)
        """
        if self.data_raw is None:
            raise Exception("No raw data available.",
                            + " Please load data via function"
                            + " 'load_big_data(...).'")

        print("EXTRACTING TRAIT & COVARIATE DATA:")

        # No information => StdValueStr == NaN AND
        #                   StdValue == NaN AND
        #                   OrigValueStr == NaN.
        num_no_info = len(self.data_raw[np.logical_and(
            self.data_raw.StdValue.isna(),
            self.data_raw.OrigValueStr.isna()
        )])

        print("Separating trait and covariate data ...", end=" ")
        # Separate trait data from covariate data.
        # Trait data have associated TraitIDs as well as DataIDs
        # while covariate data have DataIDs only and no TraitIDs.
        # So, if a row has a TraitID, it contains a trait value,
        # Else, if it contains a covariate value.
        data_trait = self.data_raw[self.data_raw.TraitID.notna()]
        data_covariate = self.data_raw[self.data_raw.TraitID.isna()]
        num_data_trait = len(data_trait)

        # Keep only those traits that are in keep_ids.
        data_trait = data_trait[
            data_trait.TraitID.isin(self.keep_ids["trait"])]
        num_data_trait = len(data_trait)
        
        # Keep only those covariate data rows that are associated 
        # with loaded trait related observations.
        data_covariate = data_covariate[
            data_covariate.ObservationID.isin(
                data_trait.ObservationID.dropna().unique())]
        num_data_covariate = len(data_covariate)
        print("done.")

        print("Noting down unique LonLat DataIDs ...", end=" ")
        # Update self.known_ids and self.keep_ids for 'lonlat' data.
        df_lonlat = []
        for coord in ["longitude", "latitude"]:
            ids_coord = _get_covariate_matches(
                data_covariate, [coord], False)
            df_coord = data_covariate[
                data_covariate.DataID.isin(ids_coord)
            ][["DataID", "DataName"]]
            df_coord = df_coord.dropna(subset="DataID")
            df_coord = df_coord.drop_duplicates()
            df_coord.columns = ["id", "name"]
            df_coord.insert(loc=len(df_coord.columns),
                            column="coordinate", value=coord[:3])
            df_lonlat.append(df_coord)
        df_lonlat = pd.concat(df_lonlat)
        df_lonlat = df_lonlat.reset_index(drop=True)
        self.known_ids["lonlat"] = df_lonlat
        self.keep_ids["lonlat"] = df_lonlat.id.tolist()
        print("done.")
    
        print("Noting down unique Year DataIDs ...", end=" ")
        # Update self.known_ids and self.keep_ids for 'year' data.
        ids_year = _get_covariate_matches(
            data_covariate, ["year", "date"], False)
        df_year = data_covariate[
            data_covariate.DataID.isin(ids_year)
        ][["DataID", "DataName"]]
        df_year = df_year.dropna(subset="DataID")
        df_year = df_year.drop_duplicates()
        df_year.columns = ["id", "name"]
        df_year = df_year.reset_index(drop=True)
        self.known_ids["year"] = df_year
        self.keep_ids["year"] = df_year.id.tolist()
        print("done.")

        print("Separating standardized and non-standardized data ...",
              end=" ")
        # Separate trait and covariate data into standardized
        # and non-standardized data.
        # Standardized data => StdValue != NaN OR StdValueStr != NaN.
        # Non standardized data => StdValue == StdValueStr == NaN
        #                          AND OrigValueStr != NaN.
        data_trait = {
            "std": data_trait[
                data_trait.StdValue.notna()],
            "non_std": data_trait[np.logical_and(
                data_trait.OrigValueStr.notna(),
                data_trait.StdValue.isna())]}
        data_covariate = { 
            "std": data_covariate[
                data_covariate.StdValue.notna()],
            "non_std": data_covariate[np.logical_and(
                data_covariate.OrigValueStr.notna(),
                data_covariate.StdValue.isna())]}
        print("done.")

        print("Adding column 'value_form' ...", end=" ")
        # Add a value form column.
        for s in ["std", "non_std"]:
            value_col_name = "StdValue" if s == "std" else "OrigValueStr"
            data_trait[s] = data_trait[s].assign(
                value_form = data_trait[s][
                    value_col_name].apply(self._get_form))
            data_covariate[s] = data_covariate[s].assign(
                value_form = data_covariate[s][
                    value_col_name].apply(self._get_form))
        print("done.")

        # Save loaded trait and covariate data in attributes.
        self.data_trait = data_trait
        self.data_covariate = data_covariate
        
        # Optionally print separated data details.
        if verbose:
            num_total = len(self.data_raw)
            print(
                f"Total no. of raw data points. = {num_total}\n",
                f"No. of trait data points. = {num_data_trait}\n",
                "No. of standardized trait data points. = ",
                f"{len(data_trait['std'])}\n",
                "No. of non standardized trait data points. = ",
                f"{len(data_trait['non_std'])}\n",
                "No. of covariate data points with ObservationID",
                "matching that of at least 1 row of trait data. = ",
                f"{num_data_covariate}\n",
                "No. of standardized such covariate data points. = ",
                f"{len(data_covariate['std'])}\n",
                "No. of non standardized such covariate",
                f"data points. = {len(data_covariate['non_std'])}\n",
                f"No. of data points with no data. = {num_no_info}\n",
                f"Loaded TraitIDs: {self.keep_ids['trait']}\n",
                f"Identified LonLat DataIDs: {self.keep_ids['lonlat']}\n",
                f"Identified Year DataIDs: {self.keep_ids['year']}",
                sep="")
                        
        print("ALL DONE :3")
    
    def extract_lonlat_data(self, verbose=True):
        """ Extracts latitude and longitude data.
        
        Standardized and non-standardized longitude and 
        latitude data associated keep_ids so extracted,
        gets stored in the data_lonlat attribute.

        Keyword Arguments:
        verbose {bool} -- Whether or not to print information about
                          loaded data. (Default True)
        """
        print("EXTRACTING LON LAT DATA ...")
        ids_lonlat = self.known_ids["lonlat"]
        ids_lonlat = ids_lonlat[
            ids_lonlat.id.isin(self.keep_ids["lonlat"])]
        data_lonlat = {"lon":{}, "lat":{}}
        for c in ["lon", "lat"]:
            for s in ["std", "non_std"]:
                data_lonlat[c][s] = self.data_covariate[s][
                    self.data_covariate[s].DataID.isin(
                        ids_lonlat[ids_lonlat.coordinate == c].id)]
        self.data_lonlat = data_lonlat
        if verbose:
            for c in ["lon", "lat"]:
                for s in ["std", "non_std"]:
                    print(f"No. of {s} {c} data rows. =",
                        len(self.data_lonlat[c][s]))
        print("ALL DONE :3")

    def extract_year_data(self, verbose=True):
        """ Extracts year data.
        
        Standardized and non-standardized year data associated with
        keep_ids so extracted, gets stored in the data_year attribute.

        Keyword Arguments:
        verbose {bool} -- Whether or not to print information about
                          loaded data. (Default True)
        """
        print("EXTRACTING YEAR DATA ...")
        data_year = {}
        for s in ["std", "non_std"]:
            data_year[s] = self.data_covariate[s][
                self.data_covariate[s].DataID.isin(self.keep_ids["year"])]
        self.data_year = data_year
        if verbose:
            for s in ["std", "non_std"]:
                print(f"No. of {s} data rows. = {len(self.data_year[s])}")
        print("ALL DONE :3")

    def lonlat_utm_to_decimal_degrees(self):
        """ Converts UTM lonlat values into decimal degrees.

        NOTE: Only rows with OrigUnitStr = 
              "utm zone_[integer] hemisphere_[n/s]" will be considered.
        """
        data_lonlat = copy.deepcopy(self.data_lonlat)
        # Extract and merge utm lat lon data into a single data frame.
        utm_data = {"lon": None, "lat": None}
        for l in ["lon", "lat"]:
            l_non_std = data_lonlat[l]["non_std"]
            utm_data[l] = l_non_std[
                l_non_std.OrigUnitStr.astype(str).str.contains("utm")
            ][["ObservationID", "ObsDataID", 
               "OrigValueStr", "OrigUnitStr"]]
        utm_data = pd.merge(left=utm_data['lon'],
                            right=utm_data['lat'],
                            how="inner",
                            on=["ObservationID", "OrigUnitStr"],
                            suffixes=["_lon", "_lat"])
        utm_data = utm_data.drop_duplicates()

        # Extract utm zone and hemisphere information from standardized units.
        utm_data = utm_data.assign(
            zone = utm_data.OrigUnitStr.apply(
                lambda n: int(n.split()[1].replace("zone_", ""))),
            hemisphere = utm_data.OrigUnitStr.apply(
                lambda n: n.split()[2].replace("hemisphere_", "")))

        # Compute decimal degrees
        decdeg_lonlat = utm_data.apply(
            lambda r: _wgs84_m_utm_to_decimal_degrees(
                r.OrigValueStr_lon, r.OrigValueStr_lat, 
                r.zone, r.hemisphere)
            , axis=1)
        utm_data = utm_data.assign(
            decdeg_lon = decdeg_lonlat.iloc[:, 0],
            decdeg_lat = decdeg_lonlat.iloc[:, 1])
        utm_data = utm_data.dropna(subset=["decdeg_lon", "decdeg_lat"])
        
        # Add newly converted latitude and longitude
        # values to data_latlon in a new column "utm2dd".
        for l in ["lon", "lat"]:
            utm_data_l = utm_data[[f"ObsDataID_{l}", f"decdeg_{l}"]]
            utm_data_l = utm_data_l.rename(columns = {
                f"ObsDataID_{l}": "ObsDataID", f"decdeg_{l}": "utm2dd"})
            data_lonlat[l]["non_std"] = pd.merge(
                left=data_lonlat[l]["non_std"], 
                right=utm_data_l, how="left", on="ObsDataID")

            # Update copy of main data frame values with UTM values
            # that have just been transformed into decimal degrees.
            new_data_l = data_lonlat[l]["non_std"].assign(
                OrigValueStr = data_lonlat[l]["non_std"].apply(
                    lambda r: r.utm2dd 
                              if r.utm2dd == r.utm2dd 
                              else r.OrigValueStr
                    , axis=1),
                OrigUnitStr = data_lonlat[l]["non_std"].apply(
                    lambda r: "decimal degrees" 
                              if r.utm2dd == r.utm2dd
                              else r.OrigUnitStr
                    , axis=1),
                value_form = data_lonlat[l]["non_std"].apply(
                    lambda r: self._get_form(r.OrigValueStr) 
                              if r.utm2dd == r.utm2dd
                              else r.value_form
                    , axis=1))
            data_lonlat[l]["non_std"] = new_data_l
            data_lonlat[l]["non_std"].drop(["utm2dd"], axis=1, 
                                           inplace=True)

            # Replace any remaining UTM values with NaN.
            utm_data_l_nan = data_lonlat[l]["non_std"]
            utm_data_l_nan = utm_data_l_nan.assign(
                OrigValueStr = utm_data_l_nan.apply(
                    lambda r: np.nan
                              if "utm" in str(r.OrigUnitStr).lower()
                              else r.OrigValueStr
                , axis=1))
            
            # APPLY CHANGES
            self.data_lonlat[l]["non_std"] = utm_data_l_nan

    def lonlat_nztm_to_decimal_degrees(self):
        """ Converts NZTM lonlat values into decimal degrees.

        NOTE: Only rows with OrigUnitStr = 'nztm' will be considered.
        """
        data_lonlat = copy.deepcopy(self.data_lonlat)
        # Extract and merge utm lat lon data into a single data frame.
        nztm_data = {"lon": None, "lat": None}
        for l in ["lon", "lat"]:
            l_non_std = copy.deepcopy(data_lonlat[l]["non_std"])
            nztm_data[l] = l_non_std[
                l_non_std.OrigUnitStr.astype(str) == "nztm"
            ][["ObservationID", "ObsDataID", "OrigValueStr", "OrigUnitStr"]]
        nztm_data = pd.merge(left=nztm_data['lon'],
                             right=nztm_data['lat'],
                             how="inner",
                             on=["ObservationID", "OrigUnitStr"],
                             suffixes=["_lon", "_lat"])
        nztm_data = nztm_data.drop_duplicates()

        # Compute decimal degrees
        decdeg_lonlat = nztm_data.apply(
            lambda r: _nztm_to_decimal_degrees(
                r.OrigValueStr_lon, r.OrigValueStr_lat)
            , axis=1)
        nztm_data = nztm_data.assign(
            decdeg_lon = decdeg_lonlat.iloc[:, 0],
            decdeg_lat = decdeg_lonlat.iloc[:, 1])
        nztm_data = nztm_data.dropna(subset=["decdeg_lon", "decdeg_lat"])

        # Add newly converted latitude and longitude
        # values to data_latlon in a new column "nztm2dd".
        for l in ["lon", "lat"]:
            nztm_data_l = nztm_data[[f"ObsDataID_{l}", f"decdeg_{l}"]]
            nztm_data_l = nztm_data_l.rename(columns = {
                f"ObsDataID_{l}": "ObsDataID", f"decdeg_{l}": "nztm2dd"})
            data_lonlat[l]["non_std"] = pd.merge(
                left=data_lonlat[l]["non_std"], 
                right=nztm_data_l, how="left", on="ObsDataID")

            # Update main data frame values with UTM values
            # that have just been transformed into decimal degrees.
            new_data_l = data_lonlat[l]["non_std"].assign(
                OrigValueStr = data_lonlat[l]["non_std"].apply(
                    lambda r: r.nztm2dd 
                              if r.nztm2dd == r.nztm2dd 
                              else r.OrigValueStr
                    , axis=1),
                OrigUnitStr = data_lonlat[l]["non_std"].apply(
                    lambda r: "decimal degrees" 
                              if r.nztm2dd == r.nztm2dd
                              else r.OrigUnitStr
                    , axis=1),
                value_form = data_lonlat[l]["non_std"].apply(
                    lambda r: self._get_form(r.OrigValueStr) 
                              if r.nztm2dd == r.nztm2dd
                              else r.value_form
                    , axis=1))
            data_lonlat[l]["non_std"] = new_data_l
            data_lonlat[l]["non_std"].drop(["nztm2dd"], axis=1, 
                                           inplace=True)

            # Replace any remaining NZTM values with NaN.
            nztm_data_l_nan = data_lonlat[l]["non_std"]
            nztm_data_l_nan = nztm_data_l_nan.assign(
                OrigValueStr = nztm_data_l_nan.apply(
                    lambda r: np.nan
                              if str(r.OrigUnitStr) == "nztm" 
                              else r.OrigValueStr
                , axis=1))
            
            # APPLY CHANGES
            self.data_lonlat[l]["non_std"] = nztm_data_l_nan

    def apply_transformations(self, data_type):
        """ Applies all configured transformations.

        NOTE: Configured transformations must be 
              DFColValTransformation objects.
        All transformations configured for "lonlat" data will
        be applied to both longitude and latitude data.

        Keyword Arguments:
        data_type {str} -- Type of data whose transformations are
                           to be applied to data stored in attribute.
                           Valid options include 'trait', 'lonlat', 
                           or 'year'.
        """
        # Validating arguments.
        _validate_data_type(data_type)
                
        print("APPLYING TRANSFORMATIONS:")
        for std_type in ["non_std", "std"]:
            std_lbl = ("standardized" if std_type == "std"
                       else "non-standardized")
            t_list = self.transforms[std_type][data_type]
            if len(t_list) > 0:
                print(f"Transforming {std_lbl} {data_type} data ...",
                      end=" ")
                for t in t_list:
                    if data_type == "trait":
                        self.data_trait[std_type] = t(
                            self.data_trait[std_type])
                    elif data_type == "lonlat":
                        for l in ['lon', 'lat']:
                            self.data_lonlat[l][std_type] = t(
                                self.data_lonlat[l][std_type])
                    else: # data_type == "year"
                        self.data_year[std_type] = t(
                            self.data_year[std_type])
                print("done.")
        print("ALL DONE :3")

    def combine_data(self, verbose=True):
        """ Combines trait, lonlat, and year data.

        Keyword Arguments:
        verbose {bool} -- Whether or not to print information
                          about combined data. (Default True) 
        
        Returns:
        {pandas.DataFrame} -- Single data frame with all 
                              standardized values.
        """
        # Get standardized feature unit.
        feature_unit = self.get_feature_unit()
        feature_col_name = (
            f"{self.feature_name}_{feature_unit}" 
            if feature_unit != "" else self.feature_name)

        # Combine standardized and non standardized data.
        data_trait = pd.concat([
            self.data_trait["std"].rename(
                columns={"StdValue": feature_col_name}),
            self.data_trait["non_std"].rename(
                columns={"OrigValueStr": feature_col_name})])
        data_trait = data_trait.dropna(subset=[feature_col_name])
        data_trait = data_trait.drop_duplicates()
        data_trait = data_trait[["ObservationID", "AccSpeciesID",
                                 feature_col_name]]
        
        data_year = pd.concat([
            self.data_year["std"].rename(
                columns={"StdValue": "year"}),
            self.data_year["non_std"].rename(
                columns={"OrigValueStr": "year"})])
        data_year = data_year.dropna(subset=["year"])
        data_year = data_year.drop_duplicates()
        data_year = data_year[["ObservationID", "AccSpeciesID", "year"]]
        
        data_lon = pd.concat([
            self.data_lonlat["lon"]["std"].rename(
                columns={"StdValue": "lon"}), 
            self.data_lonlat["lon"]["non_std"].rename(
                columns={"OrigValueStr": "lon"})])
        data_lon = data_lon.dropna(subset=["lon"])
        data_lon = data_lon[["ObservationID", "AccSpeciesID", "lon"]]
        data_lon = data_lon.drop_duplicates()
   
        data_lat = pd.concat([
            self.data_lonlat["lat"]["std"].rename(
                columns={"StdValue": "lat"}), 
            self.data_lonlat["lat"]["non_std"].rename(
                columns={"OrigValueStr": "lat"})])
        data_lat = data_lat.dropna(subset=["lat"])
        data_lat = data_lat[["ObservationID", "AccSpeciesID", "lat"]]
        data_lat = data_lat.drop_duplicates()
        
        data_lonlat = pd.merge(
            left=data_lon, right=data_lat, 
            on=["ObservationID", "AccSpeciesID"], how="inner")
        data_lonlat = data_lonlat.dropna(subset=["lon", "lat"])
        data_lonlat = data_lonlat.drop_duplicates()
        data_lonlat = data_lonlat[["ObservationID", "AccSpeciesID", 
                                   "lon", "lat"]]

        # Merge trait, lonlat, and year data.
        data = pd.merge(left=data_trait, right=data_lonlat,
                        on=["ObservationID", "AccSpeciesID"], 
                        how="left")
        data = pd.merge(left=data, right=data_year,
                        on=["ObservationID", "AccSpeciesID"], 
                        how="left")
        data = data.rename(columns={"AccSpeciesID": "species_id"})
        data = data.drop(["ObservationID"], axis=1)

        # Only return values where the feature column are not nan.
        data = data.dropna(subset=[feature_col_name])
        data = data.drop_duplicates()

        if verbose:
            print("year value range =", data.year.dropna().astype(
                int).describe()[["min", "max"]].to_dict())
            print("lon value range =", data.lon.dropna().astype(
                float).describe()[["min", "max"]].to_dict())
            print("lat value range =", np.round(data.lat.dropna().astype(
                float).describe()[["min", "max"]], 2).to_dict())
            print("no. of rows =", len(data))
            print("no. of unique species IDs =", len(
                data.species_id.dropna().unique()))
            print("no. of unique (lon, lat) combinations =", len(
                data[["lon", "lat"]].dropna().drop_duplicates()))
            print("no. of (lon, lat) combinations =", len(
                data[["lon", "lat"]].dropna()))
            if self.d_type == "float":
                print(f"{feature_col_name} value range =", data[
                    feature_col_name].dropna().astype(
                        float).describe()[["min", "max"]].to_dict())
            elif self.d_type == "int":
                print(f"{feature_col_name} value range =", data[
                    feature_col_name].dropna().astype(
                        int).describe()[["min", "max"]].to_dict())
            else: # self.d_type == "str"
                print(f"no. of unique {feature_col_name} values =", len(
                    data[feature_col_name].dropna().unique()))
                
        return data

    def avg_trait_values(self, data_type, id1, id2):
        """ Replace trait values with their average.

        Replaces trait value of both given trait IDs 
        with their average value in both standardized
        and non-standardized data if possible.
        
        Keyword Arguments:
        data_type {str} -- Type of data. Valid options include [
                           "trait", "lonlat", "year"].
        id1 {int} -- First Trait/DataID.
        id2 {int} -- Second Trait/DataID.
        """
        # Validate keyword arguments.
        _validate_data_type(data_type)
        data_id_col = "DataID" if data_type in [
            "lonlat", "year"] else "TraitID"
        
        data = copy.deepcopy(self.data_trait)
        if data_type == "lonlat":
            data = copy.deepcopy(self.data_lonlat)
        elif data_type == "year":
            data = copy.deepcopy(self.data_year)

        for std_type in  ["std", "non_std"]:
            data_val_col = ("StdValue" 
                            if std_type == "std" 
                            else "OrigValueStr")
            data_avg = None
            if data_type in ["trait", "year"]:
                data_id1 = data[std_type][
                    data[std_type][data_id_col] == id1][[
                        "ObservationID", "ObsDataID", data_val_col]]
                data_id1 = data_id1.rename(columns={
                    data_val_col: "first"})
                data_id2 = data[std_type][
                    data[std_type][data_id_col] == id2][[
                        "ObservationID", "ObsDataID", data_val_col]]
                data_id2 = data_id2.rename(columns={
                    data_val_col: "second"})
                data_avg = pd.merge(
                    left=data_id1, right=data_id2,
                    on="ObservationID", how="inner",
                    suffixes=["_1", "_2"])
                if len(data_avg) == 0: 
                    data_avg = pd.DataFrame({"ObsDataID":[], "avg": []})
                else:
                    if not(
                        _is_float(data_avg[
                            "first"].dropna().unique()[0]) and
                        _is_float(data_avg[
                            "second"].dropna().unique()[0])):
                        raise Exception("Value type of one or both "
                                        + "ids given is not numeric.")
                    data_avg = data_avg.dropna(subset=["first", "second"])
                    data_avg = data_avg.assign(avg = data_avg[
                        ["first", "second"]].astype(float).mean(axis=1))
                    data_avg = pd.concat([
                        data_avg[["ObsDataID_1", "avg"]].rename(
                            columns={"ObsDataID_1": "ObsDataID"}),
                        data_avg[["ObsDataID_2", "avg"]].rename(
                            columns={"ObsDataID_2": "ObsDataID"})])
                data_avg = data_avg.dropna(subset="avg").drop_duplicates()
            else: # data_type == "lonlat"
                data_avg = {}
                for l in ["lon", "lat"]:
                    data_id1 = data[l][std_type][
                        data[l][std_type][data_id_col] == id1
                    ][["ObservationID", "ObsDataID", data_val_col]]
                    data_id1 = data_id1.rename(columns={
                        data_val_col: "first"})
                    data_id2 = data[l][std_type][
                        data[l][std_type][data_id_col] == id2
                    ][["ObservationID", "ObsDataID", data_val_col]]
                    data_id2 = data_id2.rename(columns={
                        data_val_col: "second"})
                    data_avg_l = pd.merge(
                        left=data_id1, right=data_id2,
                        on="ObservationID", how="inner",
                        suffixes=["_1", "_2"])
                    if len(data_avg_l) == 0: 
                        data_avg_l = pd.DataFrame({
                            "ObsDataID":[], "avg": []})
                    else:
                        if not(
                            _is_float(data_avg_l[
                                "first"].dropna().unique()[0]) and
                            _is_float(data_avg_l[
                                "second"].dropna().unique()[0])):
                            raise Exception("Value type of one or both "
                                            + "ids given is not numeric.")
                        data_avg_l = data_avg_l.dropna(
                            subset=["first", "second"])
                        data_avg_l = data_avg_l.assign(
                            avg = data_avg_l[
                                ["first", "second"]
                            ].astype(float).mean(axis=1))
                        data_avg_l = pd.concat([
                            data_avg_l[["ObsDataID_1", "avg"]].rename(
                                columns={"ObsDataID_1": "ObsDataID"}),
                            data_avg_l[["ObsDataID_2", "avg"]].rename(
                                columns={"ObsDataID_2": "ObsDataID"})])
                    data_avg[l] = data_avg_l.dropna(
                        subset="avg").drop_duplicates()
            
            # APPLY CHANGES
            if data_type == "trait":
                if len(data_avg) > 0:
                    update_data = pd.merge(
                        left=data[std_type], 
                        right=data_avg,
                        on="ObsDataID", how="inner")
                    self.data_trait[std_type] = pd.merge(
                        left=self.data_trait[std_type],
                        right=update_data[["ObsDataID", "avg"]],
                        on="ObsDataID", how="left")
                    self.data_trait[std_type][
                        data_val_col
                    ] = self.data_trait[std_type].apply(
                            lambda r: r.avg if r.avg == r.avg
                                      else r[data_val_col]
                        , axis=1)
                    self.data_trait[std_type] = self.data_trait[
                        std_type].drop(["avg"], axis=1)
            elif data_type == "year":
                if len(data_avg) > 0:
                    # Round up since floating point year 
                    # values are invalid.
                    data_avg.loc[:, "avg"] = np.ceil(data_avg.avg)
                    update_data = pd.merge(
                        left=data[std_type], 
                        right=data_avg,
                        on="ObsDataID", how="inner"
                    )
                    self.data_year[std_type] = pd.merge(
                        left=self.data_year[std_type],
                        right=update_data[["ObsDataID", "avg"]],
                        on="ObsDataID", how="left"
                    )
                    self.data_year[std_type][
                        data_val_col
                    ] = self.data_year[std_type].apply(
                            lambda r: r.avg if r.avg == r.avg
                                      else r[data_val_col]
                        , axis=1)
                    self.data_year[std_type] = self.data_year[
                        std_type].drop(["avg"], axis=1)
            else: # data_type == "lonlat"
                for l in ["lon", "lat"]:
                    if len(data_avg[l]) > 0:
                        update_data = pd.merge(
                            left=data[l][std_type], 
                            right=data_avg[l],
                            on="ObsDataID", how="inner"
                        )
                        self.data_lonlat[l][std_type] = pd.merge(
                            left=self.data_lonlat[l][std_type],
                            right=update_data[["ObsDataID", "avg"]],
                            on="ObsDataID", how="left"
                        )
                        self.data_lonlat[l][std_type][
                            data_val_col
                        ] = self.data_lonlat[
                            l][std_type].apply(
                                lambda r: r.avg if r.avg == r.avg 
                                        else r[data_val_col]
                            , axis=1)
                        self.data_lonlat[l][std_type] = self.data_lonlat[
                            l][std_type].drop(["avg"], axis=1)

def get_transformation_lonlat_std():
    """ Gets DFColValTransformation to standardize lon lat values.

    Expresses non_std lon lat values in the standard format of
    a floating point number instead of in other notation, 
    for example using degrees minutes seconds etc.
    NOTE: The returned transformation is intended for use with
    data_lonlat["non_std"] only, and will only transform
    values that have OrigUnitStr == "decimal degrees".

    Returns:
    {DFColValTransformation} -- Non-std lonlat value transformation.
    """
    return DFColValTransformation(f=_value_std_latlon_deg, 
                                  col="OrigValueStr")

def get_transformation_get_year(col_transform):
    """ Returns a DFColValTransformation that extracts year from dates.
    
    The transformation will also apply changes to the same
    given column.

    Keyword Arguments:
    col_transform {str} -- Name of column containing values 
                           to be transformed.

    Retruns:
    {DFColValTransformation} -- Extract year transformation.
    """
    def extract_year_transform(r):
        date_str = r[col_transform]
        return _extract_year(date_str)
    return DFColValTransformation(extract_year_transform, col_transform)

def get_transformation_get_value_form(col_transform):
    """ Returns a DFColValTransformation that extracts value form values.
    
    The transformation will also apply changes to column "value_form".

    Keyword Arguments:
    col_transform {str} -- Name of column containing values 
                           to be transformed.

    Retruns:
    {DFColValTransformation} -- Extract value form transformation.
    """
    def extract_value_form_transform(r):
        v = r[col_transform]
        return _get_form(v)
    return DFColValTransformation(extract_value_form_transform,
                                  "value_form")

def map_plot(data, save_path="", fig_size=(10, 10), title=""):
    """ Plots lon and lat columns of given dataframe on a map.
    
    Keyword Arguments:
    data {pandas.DataFrame} -- Pandas dataframe containing columns "lon"
                               and "lat" with values in decimal degrees
                               in the range ([-180, 180], [-90, 90]).
    save_path {str} -- Saves the generated map to the given
                       location as a png image. By default,
                       the map is not saved as save_path = "".
                       (Default "")
    title {str} -- Map title. (Default "")
    fig_size {tuple} -- Size of the figure. (Default (10, 10))
    """ 
    # Drop NaN latitude and longitude values.
    data = data.dropna(subset=["lat", "lon"])
    
    # Define figure and axes.
    _, ax = plt.subplots(
        figsize=fig_size, 
        subplot_kw={'projection': ccrs.Mercator()}
    )

    data.loc[:, "lat"] = data.lat.astype(float)
    data.loc[:, "lon"] = data.lon.astype(float)

    # Plot the data.
    ax.scatter(data['lon'], data['lat'], color='green', s=10,
               transform=ccrs.PlateCarree())

    # Add gridlines and features.
    ax.gridlines(draw_labels=True)
    ax.coastlines()

    # Optinally add a title.
    plt.title(title, fontsize=14)

    # Optionally save as png.
    if save_path != "": plt.savefig(save_path, dpi=300)
    
    # Display map.
    plt.show()

def save_data(data, dest_fold, feature_name, feature_unit="", suffix=""):
    """ Saves data frame at the given path as a .csv file.

    Keyword Arguments:
    data {pandas.DataFrame} -- Pandas dataframe to save.
    dest_fold {str} -- Destination folder in which to save data.
    feature_name {str} -- Name of the feature that this dataset 
                          records values of, and has a column named after.
    feature_unit {str} -- The standard unit of this feature. (Default "")
    suffix {str} -- Some suffix to add to the file name after a "_".
    """
    filename = feature_name
    if len(feature_unit) > 0: filename += "_" + feature_unit
    if len(suffix) > 0: filename += "_" + suffix
    data.to_csv(f"{dest_fold}/{filename}.csv", index=False)
    print(f'Saved "{feature_name}" data at "{dest_fold}/{filename}.csv".')

def is_lon_lat_on_land(lon, lat):
    """ Checks if given (lon, lat) is on land.
    
    Returns True if the given latitude and longitude
    values are both not NaN and are are valid floating
    point numbers on land. False is returned otherwise.

    Keyword Arguments:
    lat {float} -- Latitude in decimal degrees.
    lon {float} -- Longitude in decimal degrees.

    Returns:
    {bool} -- True if (lon, lat) is on land and False otherwise.
    """
    # Invalid if NaN.
    if lat != lat or lon != lon: return False
    
    # Invalid if not a valid floating point number.
    if not (_is_float(lat) and _is_float(lon)): return False
    
    # Latitude must be in the range of -90 to 90 decimal degrees.
    # Longitude must be in the range of -180 to 180 decimal degrees.
    if lat < -90 or lat > 90 or lon < -180 or lon > 180: return False

    # Only other locations on land are considered valid.
    return global_land_mask.is_land(lat = lat, lon = lon)

def load_trait_table(path):
    """ Loads TRY trait table .tsv file.

    Keyword Arguments:
    path {src} -- Path to the trait table .tsv file.
    """
    return pd.read_csv(path, sep="\t").drop(['Unnamed: 5'], axis=1)

def search_trait_table(trait_table_df, search_str_list, print_matches=True):
    """ Gets matches rows from trait table. 
    
    Returns rows of the trait table containing
    the given search string. The search has the 
    following characteristics.
    - AND search w.r.t words in each search string.
    - OR search w.r.t search strings.
    For example, search_str_list = ["specific leaf area", "sla"]
    means that all traits containing either the entire substring
    "specific leaf area" comprised of 3 words (AND operation between
    words within quotes) or the word "sla" in its name, shall be
    returned as matches.

    Keyword Arguments:
    trait_table_df {pandas.DataFrame} -- Trait table as pandas data frame.
    search_str_list {list}: List of search strings.
    print_matches {bool}: Whether or not matches should be printed.
                          (Default True)
    
    Returns:
    {pandas.Dataframe} -- Subsection of DF that matches search.
    """
    trait_desc_list = [str.lower(trait) for trait in trait_table_df.Trait]
    trait_idx_list = set([])
    for i in range(len(trait_desc_list)):
        for search_str in search_str_list:
            all_words_present = True
            for word in search_str.split():
                all_words_present &= word in trait_desc_list[i]
            if all_words_present: trait_idx_list.add(i)
    trait_idx_list = list(trait_idx_list)
    trait_table_df_subset = trait_table_df.iloc[trait_idx_list, 0:2]
    if print_matches:
        for trait_id, trait_name in trait_table_df_subset.values:
            print(f"({trait_id}) - {trait_name}")
    return trait_table_df_subset

def get_val_range(df, col, filters=[]):
    """ Returns range of values in a dataframe's column. 
    
    Keyword Arguments:
    df {pandas.DataFrame} -- Data.
    col {str} -- Name of column with float values.
    filters {list} -- List of filter functions to apply to df.
                      Each function should receive a row of 
                      the df as input and return True/False because
                      these functions will be applied using the .apply()
                      function. (Default []).

    Returns:
    (list) -- Min and max values.
    """
    data_subset = df
    for fil in filters:
        data_subset = data_subset[df.apply(fil, axis=1)]
    return data_subset[col].astype(float).describe()[
        ["min", "max"]].tolist()