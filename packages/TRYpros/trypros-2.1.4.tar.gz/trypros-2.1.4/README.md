
# TRYpros - TRY Plant Database - Data Buddy
This package comprises few classes and functions that can support extraction of trait values, geo-location information (latitude, longitude) and the "year" associated with geo-referenced plant trait data in the TRY Plant Database (Kattge, J, Bönisch, G, Díaz, S, et al. TRY plant trait database – enhanced coverage and open access. Glob Change Biol. 2020; 26: 119– 188. https://doi.org/10.1111/gcb.14904).

TRYpros was developed to support the ***TRY Data Extraction Pipeline*** as described in Sections 1 to 4 below. Section 5 informs about files "*use_case_example.pdf*" containing a use case of this package to get a sense of it in action and "*template_data_processing.ipynb*" that can be used to quickly get started with data processing in accordance with the suggested data extraction pipeline. To summarize, Section 6 provides a quick description of the intended purpose of functions provided by TRYpros. Finally, Section 7 references the TRY Plant Database.

Run `pip install TRYpros` to install this package.

## Section 1: TRY Data Extraction Pipeline
The TRY Database (DB) integrates plant trait data from several hundreds of trait datasets. As there is constant acquisition of trait datasets, new versions of the TRY database are released on a regular basis. Currently, TRY version 6 is available, which is based on more than 700 contributed datasets and provides 15 million trait records for 305,000 plant taxa (mostly species) and 2661 traits, of which geo-referenced data is available for 2136 traits.

Explore the [TRY Project Official Website](https://www.try-db.org/TryWeb/Home.php) for more information.

Following subsections describe suggested steps that can be followed to extract desired data alongside location and year related information from TRY in a semi-automated manner.

The recommended ***extraction pipeline*** comprises **3 steps** as follows.
1. Identify Desirable TraitIDs
2. Request & Download Data
3. Process Data

***Data processing*** can involve the following **7 processing steps**.
1. Environment Preparation
2. Load Data
3. Process Trait Data
4. Process Lon Lat Data
5. Process Year Data
6. Combine Data
7. Save Extracted Data

***Processing steps 3, 4, and 5***, may be further composed of the following **4 processing sub-steps**.
1. ID Review
2. Extract Data
3. Manual Investigation
4. Define & Apply Transformation Functions

The rest of this document will demonstrate and explain how functions provided by TRYpros can support the aforementioned TRY Data Extraction Pipeline

## Section 2: Identifying Desired TraitIDs
In the TRY DB, for each plant feature, there may be multiple traits that record information related to it. For example, **TraitIDs** 3115 as well as 125 both record data related to the same **feature**, Specific Leaf Area.

Data requests, generally entail making requests for specific TraitIDs. Thus, a good first course of action prior to requesting data is to determine what TraitIDs are available related to your plant feature of interest. 

The trait table from the TRY website contains the following information associated with each trait in the database. Once you've downloaded the trait table and saved it as a .tsv file, it can be loaded in, using the `load_trait_table(...)` function from TRYpros.
* `ObsNum`: Number of observations.
* `ObsGRNum`: Number of geo-referenced observations.
* `PubNum`: Number of public observations.
* `AccSpecNum`: Number of accepted species.

Next, the `search_trait_table(...)` function can be used to identify what TraitIDs in TRY have data related to your feature of interest. This function returns IDs of Traits whose names contains words from the search string list that you provide.

## Section 3: Requesting & Downloading TRY Data
Once you're sure about what TraitIDs you're interested in, make a request for all data associated with those traits corresponding to all/specific available species through the TRY website. A species list can also be found on the TRY Website. 

Each request gets assigned a unique request ID and upon review, a download link will be made available, at which point you can download requested data. 

The data downloaded from this link will contain a table with both trait related data (identified using a `TraitID` in addition to a `DataID`) as well as covariate data (metadata related to trait data observations identified using a `DataID` only; example: longitude/latitude data, datetime data, etc.). Trait and covariate variable names as entered for TRY cataloging may be found in columns `TraitName` and `DataName`. Original name of the variable as in the source dataset may be found within the `OriglName` column. The name and ID of the source dataset may be found within the `Dataset` and `DatasetID` columns respectively.

All data associated with each row if present, can be found in one or more of the following columns.
* `StdValue`: Standardized value available for standardized traits.
* `StdValueStr`: Standardized entries for textual metadata.
* `OrigValueStr`: Original (non-standardized) value as text string.

The units for these values may be found in the columns below.
* `UnitName`: Standard unit available for standardized traits.
* `OrigUnitStr`: Original (non-standardized) unit as text string.

***Find more details in the documentation file that you obtain along with the .txt data file upon download. It is highly recommended that you familiarize yourself with this document well before proceeding with data processing.*** This is important for many reasons like for example, in order to understand function design decisions in this package where certain columns were chosen over others.

## Section 4: Processing Downloaded Data
Of all TraitIDs in TRY, some are "standardized", meaning that their "StdValue" or "StdValueStr" columns are populated with standardized versions of values in their "OrigValueStr" column such that all these values are expressed using the same notation, and in the same standard unit as would be present in the "UnitName" column. 

Not every TraitID is standardized. Many, are not, and thus, would need to be standardized to match their standardized counterparts wherever possible, in order for the data to be consistent, unambiguous and therefore, at its most useful. 

Some of the data values, may also be erroneous, or invalid. These must also be screened for and filtered. 

These are some of the activities that shall comprise data processing. The following sub-sections shall go over the 7 steps involved in data processing alongside TRYpros functionality that can be used with each one.

***NOTE:*** It is highly recommended that the docstring associated with each function be read before using it to learn about the full extend of what can be done using it. The following text, only briefly demonstrates how the package can be used. The docstring *MUST* be read to understand how to really use each function and their extended capabilities. Use the `help([function name])` function to do this.

### 4.1. Prepare Environment
This step involves setting values of global constants like DIR_DATA to store the path to the directory containing TRY data, etc.

In order to use most TRYpros functions, it is important to create a `FeatureHandler` object. This should therefore be done now.

``` (python)
# DEFINE FEATURE HANDLER
FH = TRYpros.FeatureHandler(
    path_src=PATH_SRC, path_ref=PATH_REF,
    feature_name=FEATURE_NAME, d_type=FEATURE_TYPE)
```

### 4.2. Load Data
This step involves loading the often large data files downloaded from TRY into memory. the `load_big_data` function of the `FeatureHandler` class allows for this.

``` (python)
# LOAD DATA
FH.load_big_data(drop_cols=DROP_COLS)
```

Data so loaded is stored in the `FeatureHandler`'s `data_raw` attribute.

It is possible that the dataset is too large to load at once. In this case the `chunk_size` and `chunk_range` attributes of the `load_big_data` function can be altered to load data in parts.

### 4.3. Process Trait Data
This step involves examining and cleaning trait data.

#### 4.3.1. ID Review
The `FeatureHandler` has 2 attributes `known_ids` and `keep_cols`. Attribute `known_ids` stores 3 dataframes each for "trait", "lonlat", and "year" related Trait/Data IDs that have been detected alongside the name of that ID in all data loaded so far. 

After the Load Data step above, only `known_ids["trait"]` will be populated. It might be that you decide not to consider some of the traits later on. If so, you can update the `keep_cols["traits"]` list to include only the IDs of traits you'd like to consider (load into the `FeatureHandler`'s `data_trait` attribute and extract data from).

``` (python)
# VIEW KNOWN IDS
print(f"Keep IDs = {FH.keep_ids["trait"]}")
FH.known_ids["trait"]

# OPTIONALLY UPDATE keep_ids.
FH.keep_ids["trait"] = [2, 1241, 231, ...]
```

#### 4.3.2. Extract Data
This step involves extracting trait data from raw loaded data and separating it from covariate data (metadata including lon lat data and year data). The `FeatureHandler`'s `extract_trait_covariate_data` function can be used to do this.

``` (python)
# EXTRACT TRAIT DATA & COVARIATE DATA (METADATA)
FH.extract_trait_covariate_data()
```

Data so loaded, populates the `data_trait = {"std": ..., "non_std": ...}` and `data_covariate = {"std": ..., "non_std": ...}` attributes of the `FeatureHandler`. Data thereby gets separated into 4, based on whether they are 1. directly related to traits, 2. or not, and 3. is standardized, 4. or not. This function also populates `FeatureHandler` attributes `known_ids['lonlat']` and `known_ids['year']` as covariate data is parsed for longitude/latitude data and year (date related) data.

#### 4.3.3. Manual Investigation
This shall perhaps the most tedious step. It involves exploring loaded trait data in the `FeatureHandler`'s `data_trait` attribute to determine if standardized value exist, and if so, what they look like as well as what processing steps might be required to standardize non-standardized data into a single most useful format for your desired purposes.

Following are examples of functions that TRYpros provides, that can be used to aid in this investigatory/exploratory quest to understand the data. 

``` (python)
# QUESTION: Are values numeric/categorical? What forms are they in?
FH.view_units_value_forms(data_type="trait")

# QUESTION: What contextual information is available?
FH.get_context(FH.data_trait["non_std"])

# QUESTION: What does data associated with specific value forms look like?
FH.get_unique_matches(
    data=FH.data_trait["non_std"],
    match_col='value_form',
    to_match=["na", "/", ".", "-"])
```

You would likely extend this section by asking more specific questions about the data tailed to your needs before proceeding to the next step.

#### 4.3.4 Define & Apply Transformation Functions
Once you've identified how units (column UnitName/OrigUnitStr) / values (column StdValue/OrigValueStr) need to be transformed as part of processing, these functions can be turned into a `DFColValTransformation` object. 

The `FeatureHandler` can then be configured to apply a series of such transformations by adding one or more `DFColValTransformation` objects to its `transforms = {"std": {"trait":[], "lonlat":[], "year":[]}, "non_std": {"trait":[], "lonlat":[], "year":[]}}` attribute under the right type of data. Configured transformations are applied using the `apply_transformations` function of the `FeatureHandler`.

It is recommended that these transformations be tested on target data by calling `transformation_obj(data)` and observing the results before applying the data. The `data_trait` attribute should also be examined after all transformations have been applied to ensure that the result is as expected.s

All these steps together in code, may look as follows.

``` (python)
# DEFINE DATA TRANSFORMATIONS
def example_unit_standardization_function(r):
    """ Maps alternate unit notations to one standard notation. """
    unit = r.OrigUnitStr
    if unit == unit: # Not NaN.
        if unit in ["mm2 mg-1", "mm2/mg"]: 
            return "mm^{2}mg^{-1}"
        if unit in ['m2/kg', 'm2 kg-1']:
            return "m^{1}kg^{-1}"
        if unit in ['cm2/g']:
            return 'cm^{2}g^{-1}'
        if unit in ['g/cm2', "(g/cm2)"]:
            return 'g^{1}cm^{-2}'
    return unit

# WRAP EACH TRANSFORMATION FUNCTION IN 
# ONE DFColValTransformation OBJECT
t_unit_std = TRYpros.DFColValTransformation(
    f=example_unit_standardization_function, 
    col="OrigUnitStr")

# TEST TRANSFORMATIONS BEFORE APPLICATION
res_t = FH.data_trait["non_std"]
res_t = t_unit_std(res_t)
print(res_t.value_form.unique())

# CONFIGURE TRANSFORMATIONS
# Add each transformation object to list of transformations to be 
# applied to each data type and standardization type.
FH.transforms["non_std"]["trait"] = [t_unit_std]

# APPLY CONFIGURED TRANSFORMATIONS
FH.apply_transformations("trait")

# CHECK SUCCESSFUL APPLICATION
FH.data_trait["non_std"].OrigValueStr.unique()
```

***NOTE:*** The example code above configures one transformation for non-standardized data. This is for demonstration purposes only. In reality, as many transformations as required can be applied sequentially to both standardized and non-standardized data. This is why the `transform` attribute of the `FeatureHandler` has both an `std` and `non_std` key. Also, above suggested methods of checking correctness are just examples. In reality, more thorough investigation may be required to judge with transformations were indeed correctly applied or not.

### 4.4. Process Lon Lat Data
This step involves extracting and processing longitude and latitude metadata related to considered TraitIDs (relates = longitude or latitude DataID row has same ObservationID as that of a TraitID row). 

The 4 steps involves are similar to the 4 steps under trait data processing above.

#### 4.4.1. ID Review
This step, as before, involves looking at known IDs (DataIDs instead of TraitIDS now since lon lat data is covariate data and not main trait data) and deciding which ones to consider for further processing and which ones to ignore.

``` (python)
# VIEW KNOWN IDS
print(f"Keep IDs = {FH.keep_ids["lonlat"]}")
FH.known_ids["lonlat"]

# OPTIONALLY UPDATE IDs TO KEEP
FH.keep_ids["lonlat"] = [...]
```

#### 4.4.2. Extract Data
This step involves populating the `FeatureHandler`'s `data_lonlat` attribute with lonlat data extracted from `data_covariate`. This data is stored separated into categories `longitude`, `latitude`, `std` and `non_std` as `data_lonlat = {"longitude":{"std": ..., "non_std": ...}, "latitude": {"std": ..., "non_std": ...}}`.

``` (python)
# EXTRACT LON LAT DATA
FH.extract_lonlat_data()
```

#### 4.4.3. Manual Investigation
Manual investigation can differ on a case by case basis, but in general can use the following functions as with trait data previously. 

That said, since lonlat data has a longitude and latitude part, it can be harder to explore. So, a function, `get_combine_lonlat` from the `FeatureHandler` can be used to combine these together based on standardization category (std or non_std).

Also, it was observed while working with TRY data, that some lon lat values may be expressed in formats other than the generally standard, decimal degree. Most common alternate formats are UTM/WGS84 and NZTM (New Zealand Transverse Meridian). Thus, functions have been provided to extract rows associated with these formats based on clues from context columns like 'DataName', 'OriglName', and 'Comment'.

``` (python)
# CONSIDER COMBINING LON LAT DATA FOR EASIER INVESTIGATION
data_latlon_std = FH.get_combine_lonlat("std")
data_latlon_non_std = FH.get_combine_lonlat("non_std")

# QUESTION: What do value units and forms look like?
FH.view_units_value_forms(data_type="lonlat")

# QUESTION: Do some columns provide useful context information?
FH.get_context(data_latlon_non_std)

# QUESTION: What are all the different forms of value expression?
data_latlon_non_std.value_form.unique()

# QUESTION: What data is available in the UTM format?
data_utm = FH.get_utm_data()
data_utm

# QUESTION: What data is available in the NZTM format?
data_nztm = FH.get_nztm_data()
FH.get_context(data_nztm)
```

#### 4.4.4. Define & Apply Transformation Functions
This step, also as before involves creating unit/value transformation functions informed by observations in the previous step, wrapping them in `DFColValTransformation` and testing them prior to applying to loaded data and checking to ensure successful application.

For lonlat data, it is very normal for both standardized and non-standardized data to be expressed in various notations ("x°y'z''", "89.3213", "xd ym zs", etc.) even though conveying the same "degrees" information. So, TRYPros provides a function `get_transformation_lonlat_std` that can be used to fetch a transformation object that can directly be used to configure `FH.transforms["non_std"/"std"]["lonlat"]` to convert these alternate notations into a standard format. This standard format is the floating point number notation since it is generally accepted to represent longitude/latitude values in the range [-180, 180]/[-90, 90] respectively, and this is generally (NOTE: not always) the case with standardized lonlat values anyway.

Also, since transformation objects often change the value associated with a row, the `value_form` function that represent the general form of the function will no longer be representative of the truth once the values are updated. Thus, the `FeatureHandler` makes available, a `get_transformation_get_value_form` function that returns a transformation object that recomputes column "value_form".

``` (python)
# DEFINE FUNCTIONS
ll_val_std_deg = TRYpros.get_transformation_lonlat_std()
ll_form_recompute = TRYpros.get_transformation_get_value_form("OrigValueStr")

# TEST TRANSFORMATIONS PRIOR TO APPLICATION
print("Unique Value Forms (Before):", 
      data_latlon_non_std.value_form.unique())
res_ll = data_latlon_non_std
res_ll = ll_val_std_deg(res_ll)
res_ll = ll_form_recompute(res_ll)
print("Unique Value Forms (After):", 
      res_ll.value_form.unique())

# CONFIGURE TRANSFORMATIONS
FH.transforms["non_std"]["lonlat"] = [ll_val_std_deg, ll_form_recompute]

# APPLY TRANSFORMATIONS
FH.apply_transformations("lonlat")
```

In the TRY dataset, all data (trait and covariate) are present in long form, meaning that they are all placed one row after another (longitude rows may be mixed in with latitude rows) such that the dataset does not have longitude and latitude values neatly separated into columns.

Thus, a transformation object that applies the same transformation function to every value in a column, cannot serve to convert UTM/NZTM formats into decimal degrees because both longitude and latitude values related to each measurement (ObservationID) is required to do this. Thus, in such cases, which are fairly common, processing is more involved. To make this easier, TRYpros's `FeatureHandler` provides functions `lonlat_utm_to_decimal_degrees()` and `lonlat_nztm_to_decimal_degrees()` to perform this conversion for you. These functions extract UTM/NZTM lon lat values associated with each unique observation and then use them to compute the decimal degrees (the standard) equivalent and then update corresponding row values in the `data_lonlat` attribute to reflect this.

Additionally, it has also been noticed that sometimes, DataIDs/TraitIDs are measured in min-max or first-last pairs. For example: DataID 4710 => minimum Longitude and DataID 4711 = maximum Longitude. In such scenarios, it can be useful to replace these min and max values with average values. The function `avg_trait_values(...)` from `FeatureHandler` can be used to do this.

``` (python)
# OPTIONALLY PERFORM OTHER PROCESSING STEPS

# CONVERT UTM VALUES
FH.lonlat_utm_to_decimal_degrees()

# CONVERT NZTM VALUES
FH.lonlat_nztm_to_decimal_degrees()

# AVG TRAIT VALUES
FH.avg_trait_values(data_type="lonlat", id1=4710, id2=4711)
```

Once all transformations are complete, it is important to check if they were successful and if the data is now standardized and valid. One way to do this with lon lat data is to check the range of resulting values. The `view_range` function can be used to do this as follows.

``` (python)
# CHECK SUCCESSFUL APPLICATION
FH.view_range(data_type="lonlat", std_type="std")
FH.view_range(data_type="lonlat", std_type="non_std")
# If there are abnormal values, then something may be wrong.
```

### 4.5. Process Year Data
Now, just as how lonlat data was extracted from covariate data, the year during which the measurements were made can be extracted from covariate datetime data. The year is chosen because this piece of information is most common among datetime related covariate data and also because given the truly large no. of formats in which day/season/year data can be found within the TRY DB, it is most feasible to extract year only, rather than screen for and compute more precise information like day of measurement.

Processing year data involves much the same steps as processing lonlat data as seen previously.

#### 4.5.1. ID Review
This step involves viewing identified known IDs and deciding which ones to keep.

``` (python)
# VIEW KNOWN IDS
print(f"Keep IDs = {FH.keep_ids["year"]}")
FH.known_ids["year"]

# OPTIONALLY UPDATE KEEP LIST
# Only data corresponding to Trait/Data IDs in the keep list are loaded
# into the FeatureHandler's attribute (data_trait, data_lonlat, or data_year).
FH.keep_ids["year"] = [241, 212, 696, 2254, 2255, 6601, 8571, 8737, 9732]
FH.get_considered_traits("year")
```

#### 4.5.2. Extract Data
This step entails extracting data with year information from covariate data into the `FeatureHandler`'s `data_year = {'std': ..., 'non_std': ...}` attribute. It's `extract_year_data()` function can be used to do this.

``` (python)
# EXTRACT YEAR/DATE RELATED DATA
FH.extract_year_data()
```

#### 4.5.3. Manual Investigation
Here, as before, data is explored to determine transformation function that need to be defined and applied in the next step to standardized values.

``` (python)
# QUESTION: What do value units and forms look like?
FH.view_units_value_forms(data_type="year")

# QUESTION: What context information is available?
FH.get_context(FH.data_year["non_std"], context_cols=[
    "OriglName"])["OriglName"].tolist()

# QUESTION: What data is associated with specific DatasetIDs?
display(FH.get_unique_matches(
    data=FH.data_year["non_std"], match_col="DatasetID",
    to_match=[1], keep=["DataID", "OrigValueStr", "value_form"]))
display(FH.get_unique_matches(
    data=FH.data_year["non_std"], match_col="DataID",
    to_match=[241], keep=["DataID", "OrigValueStr", "value_form"]))
```

#### 4.5.4. Define & Apply Transformation Functions
This step involves creating, configuring and applying transformation objects as before.

The most common operation needed with year data, is the transformation that extracts the "year" part from different ways of expressing datetime related information in TRY (there are a ridiculously large number of these). To facilitate this, the `FeatureHandler` provides the `get_transformation_get_year` function that returns a transformation object that does just this.

``` (python)
# DEFINE TRANSFORMATIONS
y_ext_year_std = TRYpros.get_transformation_get_year("StdValue")
y_ext_year_non_std = TRYpros.get_transformation_get_year("OrigValueStr")
y_get_val_form_non_std = TRYpros.get_transformation_get_value_form("StdValue")
y_get_val_form_std = TRYpros.get_transformation_get_value_form("OrigValueStr")

# TEST TRANSFORMATIONS PRIOR TO APPLICATION
res_y = FH.data_year["non_std"]
print("before:", res_y["value_form"].unique())
res_y = y_ext_year_non_std(res_y)
res_y = y_get_val_form_non_std(res_y)
print("after:", res_y["value_form"].unique())

# CONFIGURE TRANSFORMATIONS
FH.transforms["std"]["year"] = [y_ext_year_std, y_get_val_form_std]
FH.transforms["non_std"]["year"] = [y_ext_year_non_std, y_get_val_form_non_std]

# APPLY CONFIGURED TRANSFORMATIONS
FH.apply_transformations(data_type="year")
```

Similar to the min-max case with lonlat data, it is possible that first and last date of measurement is recorded. So, it can be useful compute the mean year as follows after year extraction from dates.

``` (python)
# DECISION: Average first and last year data.
FH.avg_trait_values(data_type="year", id1=4688, id2=4691)

# CHECK TO ENSURE SUCCESS
FH.view_range(data_type="year", std_type="std")
FH.view_range(data_type="year", std_type="non_std")
```

### 4.6. Combine Data
This step involves combining extracted trait, lonlat and year data such that lon, lat, and year are added as columns to the dataset with trait data in it. The `FeatureHandler`'s `combine_data()` function can be used to do this. Furthermore, the `map_plot` function from `TRYpros` can be used to view extracted geo-coordinates on a map.

``` (python)
# COMBINE TRAIT, LONLAT AND YEAR DATA
data_extracted = FH.combine_data()

# VIEW ON MAP
TRYpros.map_plot(data_extracted, 
                 title=f"TRY Data Distribution: {FH.feature_name}")
```

### 4.7. Save Extracted Data
Once data has been extracted and processed, the combined data may be saved into a .csv file. This can be done using the `save_data(...)` function from `TRYpros`.
``` (python)
# SAVE PROCESSED EXTRACTED DATA
TRYpros.save_data(
    data = data_extracted, 
    dest_fold = PATH_DST,
    feature_name = FH.feature_name,
    feature_unit = FH.get_feature_unit())
```

## Section 5: Template & Example Use Case
Please view an example use case where the TRYpros package was used with the recommended ***Data Processing*** from the proposed ***TRY Data Extraction Pipeline*** to extract data related to the "Specific Leaf Area" plant feature in the file "*use_case_example.pdf*". TraitIDs for which data was requested for this particular use case include = [37, 1251].

Also, please find file "*template_data_processing.ipynb*" that provides a python notebook template file using with you can get started on processing downloaded data from the TRY DB using the TRYpros package.

You may find these files [here](https://drive.google.com/drive/folders/1MkzTE7W8cU5OZqhZ4hqZCIDCmbGqltI6?usp=sharing).

## Section 6: TRYpros Functionality Summarized
Following is a list of function names with a brief description of what they do. Functions accessible as part of the `FeatureHandler` object is prefixed with `FH`. As for objects of the `DFColValTransformation` class, the only function directly associated with it, is the object's own call function that would simply look like `transformation_object(data)` and hence is not part of the list below. Details like their input parameters and output must be learned by examining the doc-strings corresponding to each function. This can be fetched by using the python command `help([function name])`. 
* `load_trait_table`: Load the trait table .tsv file downloaded from TRY.
* `search_trait_table`: Search trait names in the trait table and return trait ids with names containing words in the list of words to match.
* `is_lon_lat_on_land`: Check if a given latitude and longitude corresponds to a position on land.
* `save_data`: Saves data frame (processed data) at the given path as a .csv file.
* `map_plot`:  Plot data from the "lon" and "lat" columns that are assumed to be a part of the data frame on a world map.
* `get_transformation_get_value_form`: Returns a DFColValTransformation that extracts value form values.
* `get_transformation_get_year`: Returns a DFColValTransformation that extracts year from dates.
* `get_transformation_lonlat_std`: Gets DFColValTransformation to standardize lon lat values.
* `get_val_range`: Returns range of values in a dataframe's column containing float values.
* `FH.get_chunk_count`: Gets no. of chunks of data if each chunk is the given size.
* `FH.view_units_value_forms`: Displays unit and value forms of std & non-std data.
* `FH.get_context`: Displays unique value combinations of contextual columns.
* `FH.get_unique_matches`: Get unique rows that match given column values.
* `FH.get_combine_lonlat`: Combines longitude and latitude data for easier exploration.
* `FH.get_utm_data`: Gets rows corresponding to non-std lon lat data in UTM format.
* `FH.get_nztm_data`: Gets rows corresponding to non-std lon lat data in NZTM form.
* `FH.get_feature_unit`: Gets unit from current version of standardized trait data.
* `FH.get_considered_traits`: Gets known traits currently configured to be kept. 
* `FH.view_range`: Prints data range for given std type. 
* `FH.load_big_data`: Loads a large data file. 
* `FH.extract_trait_covariate_data`: Extract trait data and separate it from covariate data.
* `FH.extract_lonlat_data`: Extracts latitude and longitude data.
* `FH.extract_year_data`: Extracts year data.
* `FH.lonlat_utm_to_decimal_degrees`: Converts UTM lonlat values into decimal degrees.
* `FH.lonlat_nztm_to_decimal_degrees`: Converts NZTM lonlat values into decimal degrees.
* `FH.apply_transformations`: Applies all configured transformations.
* `FH.combine_data`: Combines trait, lonlat, and year data.
* `FH.avg_trait_values`: Replace trait values with their average.

Following is the list of attributes in `FeatureHandler` that may be configured to adjust behavior.
* `keep_ids`: The list of IDs to keep for "trait", "lonlat", and "year" data can be updated to define what Trait/DataIDs from the list of IDs in attribute `known_ids` to consider when loading and processing data into attributes `data_trait`, `data_lonlat`, and `data_year`. All IDs not in the keep list that are in the known list, will be ignored. By default, all known IDs are included in the keep list.
* `options_value_form`: Boolean values `replace_month`, `replace_season` and `make_lowercase` can be set to change how the `value_form` column is computed. By default, all "month" name substrings (full month name like "december" or short forms like "dec") in the trait values are replaced with character 'm' when computing value form. Similarly, season name substrings (full season names like "spring" only) are replaced with the character 's'. Also by default, value_form characters will be all lowercase. In some cases, this may need to be tweaked. Whether or not to update these configurations are up to you. For example, when processing leaf phenology type data, with default value form options, the value form of the term "deciduous" will be "miduous" because "dec" matches the month short form. In such a case, it may be best to set `FH.options_value_form["replace_month"] = False`. This is therefore something important to be aware of.
* `transforms`: As demonstrated in Section 4, the transformations to apply to each type of data (trait/lonlat/year and std/non_std) is configured by adding `DFColValTransformation` objects to lists of the `FeatureHandler`'s `transforms` attribute. 

## Section 7: TRY - Complete Standard Reference
Kattge, J., G. Bönisch, S. Díaz, S. Lavorel, I. C. Prentice, P. Leadley, S. Tautenhahn, G. D. A. Werner, T.
Aakala, M. Abedi, A. T. R. Acosta, G. C. Adamidis, K. Adamson, M. Aiba, C. H. Albert, J. M. Alcántara, C.
Alcázar C, I. Aleixo, H. Ali, B. Amiaud, C. Ammer, M. M. Amoroso, M. Anand, C. Anderson, N. Anten, J.
Antos, D. M. G. Apgaua, T.-L. Ashman, D. H. Asmara, G. P. Asner, M. Aspinwall, O. Atkin, I. Aubin, L.
Baastrup-Spohr, K. Bahalkeh, M. Bahn, T. Baker, W. J. Baker, J. P. Bakker, D. Baldocchi, J. Baltzer, A.
Banerjee, A. Baranger, J. Barlow, D. R. Barneche, Z. Baruch, D. Bastianelli, J. Battles, W. Bauerle, M.
Bauters, E. Bazzato, M. Beckmann, H. Beeckman, C. Beierkuhnlein, R. Bekker, G. Belfry, M. Belluau, M.
Beloiu, R. Benavides, L. Benomar, M. L. Berdugo-Lattke, E. Berenguer, R. Bergamin, J. Bergmann, M.
Bergmann Carlucci, L. Berner, M. Bernhardt-Römermann, C. Bigler, A. D. Bjorkman, C. Blackman, C.
Blanco, B. Blonder, D. Blumenthal, K. T. Bocanegra-González, P. Boeckx, S. Bohlman, K. Böhning- Gaese,
L. Boisvert-Marsh, W. Bond, B. Bond-Lamberty, A. Boom, C. C. F. Boonman, K. Bordin, E. H. Boughton,
V. Boukili, D. M. J. S. Bowman, S. Bravo, M. R. Brendel, M. R. Broadley, K. A. Brown, H. Bruelheide, F.
Brumnich, H. H. Bruun, D. Bruy, S. W. Buchanan, S. F. Bucher, N. Buchmann, R. Buitenwerf, D. E. Bunker,
J. Bürger, S. Burrascano, D. F. R. P. Burslem, B. J. Butterfield, C. Byun, M. Marques, M. C. Scalon, M.
Caccianiga, M. Cadotte, M. Cailleret, J. Camac, J. J. Camarero, C. Campany, G. Campetella, J. A. Campos,
L. Cano-Arboleda, R. Canullo, M. Carbognani, F. Carvalho, F. Casanoves, B. Castagneyrol, J. A. Catford,
J. Cavender-Bares, B. E. L. Cerabolini, M. Cervellini, E. Chacón-Madrigal, K. Chapin, F. S. Chapin, S. Chelli,
S.-C. Chen, A. Chen, P. Cherubini, F. Chianucci, B. Choat, K.-S. Chung, M. Chytrý, D. Ciccarelli, L. Coll, C.
G. Collins, L. Conti, D. Coomes, J. H. C. Cornelissen, W. K. Cornwell, P. Corona, M. Coyea, J. Craine, D.
Craven, J. P. G. M. Cromsigt, A. Csecserits, K. Cufar, M. Cuntz, A. C. da Silva, K. M. Dahlin, M. Dainese, I.
Dalke, M. Dalle Fratte, A. T. Dang-Le, J. Danihelka, M. Dannoura, S. Dawson, A. J. de Beer, A. De Frutos,
J. R. De Long, B. Dechant, S. Delagrange, N. Delpierre, G. Derroire, A. S. Dias, M. H. Diaz-Toribio, P. G.
Dimitrakopoulos, M. Dobrowolski, D. Doktor, P. Dřevojan, N. Dong, J. Dransfield, S. Dressler, L. Duarte,
E. Ducouret, S. Dullinger, W. Durka, R. Duursma, O. Dymova, A. E- Vojtkó, R. L. Eckstein, H. Ejtehadi, J.
Elser, T. Emilio, K. Engemann, M. B. Erfanian, A. Erfmeier, A. Esquivel-Muelbert, G. Esser, M. Estiarte, T.
F. Domingues, W. F. Fagan, J. Fagúndez, D. S. Falster, Y. Fan, J. Fang, E. Farris, F. Fazlioglu, Y. Feng, F.
Fernandez-Mendez, C. Ferrara, J. Ferreira, A. Fidelis, B. Finegan, J. Firn, T. J. Flowers, D. F. B. Flynn, V.
Fontana, E. Forey, C. Forgiarini, L. François, M. Frangipani, D. Frank, C. Frenette-Dussault, G. T. Freschet,
E. L. Fry, N. M. Fyllas, G. G. Mazzochini, S. Gachet, R. Gallagher, G. Ganade, F. Ganga, P. García-Palacios,
V. Gargaglione, E. Garnier, J. L. Garrido, A. L. de Gasper, G. Gea-Izquierdo, D. Gibson, A. N. Gillison, A.
Giroldo, M.-C. Glasenhardt, S. Gleason, M. Gliesch, E. Goldberg, B. Göldel, E. Gonzalez-Akre, J. L.
Gonzalez-Andujar, A. González-Melo, A. González-Robles, B. J. Graae, E. Granda, S. Graves, W. A. Green,
T. Gregor, N. Gross, G. R. Guerin, A. Günther, A. G. Gutiérrez, L. Haddock, A. Haines, J. Hall, A.
Hambuckers, W. Han, S. P. Harrison, W. Hattingh, J. E. Hawes, T. He, P. He, J. M. Heberling, A. Helm, S.
Hempel, J. Hentschel, B. Hérault, A.-M. Hereş, K. Herz, M. Heuertz, T. Hickler, P. Hietz, P. Higuchi, A. L.
Hipp, A. Hirons, M. Hock, J. A. Hogan, K. Holl, O. Honnay, D. Hornstein, E. Hou, N. Hough-Snee, K. A.
Hovstad, T. Ichie, B. Igić, E. Illa, M. Isaac, M. Ishihara, L. Ivanov, L. Ivanova, C. M. Iversen, J. Izquierdo, R.
B. Jackson, B. Jackson, H. Jactel, A. M. Jagodzinski, U. Jandt, S. Jansen, T. Jenkins, A. Jentsch, J. R. P.
Jespersen, G.-F. Jiang, J. L. Johansen, D. Johnson, E. J. Jokela, C. A. Joly, G. J. Jordan, G. S. Joseph, D.
Junaedi, R. R. Junker, E. Justes, R. Kabzems, J. Kane, Z. Kaplan, T. Kattenborn, L. Kavelenova, E. Kearsley,
A. Kempel, T. Kenzo, A. Kerkhoff, M. I. Khalil, N. L. Kinlock, W. D. Kissling, K. Kitajima, T. Kitzberger, R.
Kjøller, T. Klein, M. Kleyer, J. Klimešová, J. Klipel, B. Kloeppel, S. Klotz, J. M. H. Knops, T. Kohyama, F.
Koike, J. Kollmann, B. Komac, K. Komatsu, C. König, N. J. B. Kraft, K. Kramer, H. Kreft, I. Kühn, D.
Kumarathunge, J. Kuppler, H. Kurokawa, Y. Kurosawa, S. Kuyah, J.-P. Laclau, B. Lafleur, E. Lallai, E. Lamb,
A. Lamprecht, D. J. Larkin, D. Laughlin, Y. Le Bagousse-Pinguet, G. le Maire, P. C. le Roux, E. le Roux, T.
Lee, F. Lens, S. L. Lewis, B. Lhotsky, Y. Li, X. Li, J. W. Lichstein, M. Liebergesell, J. Y. Lim, Y.-S. Lin, J. C.
Linares, C. Liu, D. Liu, U. Liu, S. Livingstone, J. Llusià, M. Lohbeck, Á. López-García, G. Lopez-Gonzalez, Z.
Lososová, F. Louault, B. A. Lukács, P. Lukeš, Y. Luo, M. Lussu, S. Ma, C. Maciel Rabelo Pereira, M. Mack,
V. Maire, A. Mäkelä, H. Mäkinen, A. C. M. Malhado, A. Mallik, P. Manning, S. Manzoni, Z. Marchetti, L.
Marchino, V. Marcilio-Silva, E. Marcon, M. Marignani, L. Markesteijn, A. Martin, C. Martínez-Garza, J.
Martínez- Vilalta, T. Mašková, K. Mason, N. Mason, T. J. Massad, J. Masse, I. Mayrose, J. McCarthy, M.
L. McCormack, K. McCulloh, I. R. McFadden, B. J. McGill, M. Y. McPartland, J. S. Medeiros, B. Medlyn, P.
Meerts, Z. Mehrabi, P. Meir, F. P. L. Melo, M. Mencuccini, C. Meredieu, J. Messier, I. Mészáros, J.
Metsaranta, S. T. Michaletz, C. Michelaki, S. Migalina, R. Milla, J. E. D. Miller, V. Minden, R. Ming, K.
Mokany, A. T. Moles, A. Molnár V, J. Molofsky, M. Molz, R. A. Montgomery, A. Monty, L. Moravcová, A.
Moreno-Martínez, M. Moretti, A. S. Mori, S. Mori, D. Morris, J. Morrison, L. Mucina, S. Mueller, C. D.
Muir, S. C. Müller, F. Munoz, I. H. Myers-Smith, R. W. Myster, M. Nagano, S. Naidu, A. Narayanan, B.
Natesan, L. Negoita, A. S. Nelson, E. L. Neuschulz, J. Ni, G. Niedrist, J. Nieto, Ü. Niinemets, R. Nolan, H.
Nottebrock, Y. Nouvellon, A. Novakovskiy, The Nutrient Network, K. O. Nystuen, A. O Grady, K. O Hara,
A. O Reilly-Nugent, S. Oakley, W. Oberhuber, T. Ohtsuka, R. Oliveira, K. Öllerer, M. E. Olson, V.
Onipchenko, Y. Onoda, R. E. Onstein, J. C. Ordonez, N. Osada, I. Ostonen, G. Ottaviani, S. Otto, G. E.
Overbeck, W. A. Ozinga, A. T. Pahl, C. E. T. Paine, R. J. Pakeman, A. C. Papageorgiou, E. Parfionova, M.
Pärtel, M. Patacca, S. Paula, J. Paule, H. Pauli, J. G. Pausas, B. Peco, J. Penuelas, A. Perea, P. L. Peri, A. C.
Petisco-Souza, A. Petraglia, A. M. Petritan, O. L. Phillips, S. Pierce, V. D. Pillar, J. Pisek, A. Pomogaybin,
H. Poorter, A. Portsmuth, P. Poschlod, C. Potvin, D. Pounds, A. S. Powell, S. A. Power, A. Prinzing, G.
Puglielli, P. Pyšek, V. Raevel, A. Rammig, J. Ransijn, C. A. Ray, P. B. Reich, M. Reichstein, D. E. B. Reid, M.
Réjou-Méchain, V. R. de Dios, S. Ribeiro, S. Richardson, K. Riibak, M. C. Rillig, F. Riviera, E. M. R. Robert,
S. Roberts, B. Robroek, A. Roddy, A. V. Rodrigues, A. Rogers, E. Rollinson, V. Rolo, C. Römermann, D.
Ronzhina, C. Roscher, J. A. Rosell, M. F. Rosenfield, C. Rossi, D. B. Roy, S. Royer-Tardif, N. Rüger, R. Ruiz-
Peinado, S. B. Rumpf, G. M. Rusch, M. Ryo, L. Sack, A. Saldaña, B. Salgado-Negret, R. Salguero-Gomez,
I. Santa-Regina, A. C. Santacruz-García, J. Santos, J. Sardans, B. Schamp, M. Scherer- Lorenzen, M.
Schleuning, B. Schmid, M. Schmidt, S. Schmitt, J. V. Schneider, S. D. Schowanek, J. Schrader, F. Schrodt,
B. Schuldt, F. Schurr, G. Selaya Garvizu, M. Semchenko, C. Seymour, J. C. Sfair, J. M. Sharpe, C. S.
Sheppard, S. Sheremetiev, S. Shiodera, B. Shipley, T. A. Shovon, A. Siebenkäs, C. Sierra, V. Silva, M. Silva,
T. Sitzia, H. Sjöman, M. Slot, N. G. Smith, D. Sodhi, P. Soltis, D. Soltis, B. Somers, G. Sonnier, M. V.
Sørensen, E. E. Sosinski Jr, N. A. Soudzilovskaia, A. F. Souza, M. Spasojevic, M. G. Sperandii, A. B. Stan,
J. Stegen, K. Steinbauer, J. G. Stephan, F. Sterck, D. B. Stojanovic, T. Strydom, M. L. Suarez, J.-C. Svenning,
I. Svitková, M. Svitok, M. Svoboda, E. Swaine, N. Swenson, M. Tabarelli, K. Takagi, U. Tappeiner, R. Tarifa,
S. Tauugourdeau, C. Tavsanoglu, M. te Beest, L. Tedersoo, N. Thiffault, D. Thom, E. Thomas, K.
Thompson, P. E. Thornton, W. Thuiller, L. Tichý, D. Tissue, M. G. Tjoelker, D. Y. P. Tng, J. Tobias, P. Török,
T. Tarin, J. M. Torres-Ruiz, B. Tóthmérész, M. Treurnicht, V. Trivellone, F. Trolliet, V. Trotsiuk, J. L.
Tsakalos, I. Tsiripidis, N. Tysklind, T. Umehara, V. Usoltsev, M. Vadeboncoeur, J. Vaezi, F. Valladares, J.
Vamosi, P. M. van Bodegom, M. van Breugel, E. Van Cleemput, M. van de Weg, S. van der Merwe, F.
van der Plas, M. T. van der Sande, M. van Kleunen, K. Van Meerbeek, M. Vanderwel, K. A. Vanselow, A.
Vårhammar, L. Varone, M. Y. Vasquez Valderrama, K. Vassilev, M. Vellend, E. J. Veneklaas, H. Verbeeck,
K. Verheyen, A. Vibrans, I. Vieira, J. Villacís, C. Violle, P. Vivek, K. Wagner, M. Waldram, A. Waldron, A.
P. Walker, M. Waller, G. Walther, H. Wang, F. Wang, W. Wang, H. Watkins, J. Watkins, U. Weber, J. T.
Weedon, L. Wei, P. Weigelt, E. Weiher, A. W. Wells, C. Wellstein, E. Wenk, M. Westoby, A. Westwood,
P. J. White, M. Whitten, M. Williams, D. E. Winkler, K. Winter, C. Womack, I. J. Wright, S. J. Wright, J.
Wright, B. X. Pinho, F. Ximenes, T. Yamada, K. Yamaji, R. Yanai, N. Yankov, B. Yguel, K. J. Zanini, A. E.
Zanne, D. Zelený, Y.-P. Zhao, J. Zheng, J. Zheng, K. Ziemińska, C. R. Zirbel, G. Zizka, I. C. Zo-Bi, G. Zotz and
C. Wirth (2020) TRY plant trait database – enhanced coverage and open access. Global Change Biology
26: 119 – 188. https://doi.org/10.1111/gcb.14904