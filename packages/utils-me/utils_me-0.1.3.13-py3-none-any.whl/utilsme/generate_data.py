from utilsme import genInteger, genString, genBool, genDecimal
import pandas as pd
import polars as pl

def generate_data(data_model: dict, nb_rows: int, type_dataframe: pd.DataFrame | pl.DataFrame = pl.DataFrame):
    """
    Generate a DataFrame based on the provided data model and number of rows.
    
    Args:
        data_model (dict): The data model defining the structure of the DataFrame.
        nb_rows (int): The number of rows to generate.
        type_dataframe (pd.DataFrame | pl.DataFrame): The type of DataFrame to create.
    
    Returns:
        pd.DataFrame | pl.DataFrame: The generated DataFrame.
        dict: The settings used for generating the data.
    """
    
    data_dict = {}
    data_settings = {}
    
    for key, values in data_model.items():
        if key == 'columns':
            for i in range(nb_rows):
                
                for col in values:
                    if col['name'] not in data_dict.keys():
                        data_dict[col['name']] = []
                    
                    if col['type'] == 'integer':
                        # Pass min and max to genInteger
                        min = col.get('min')
                        max = col.get('max')
                        params = {}
                        if min:
                            params['min'] = min
                        if max:
                            params['max'] = max
                        # Generate an integer value
                        data_dict[col['name']].append(genInteger(**params))
                    elif col['type'] == 'string':
                        # Pass length to genString
                        length = col.get('length')  # Default length
                        min = col.get('min')  # Default min
                        max = col.get('max')  # Default max
                        
                        params = {}
                        if min:
                            params['min'] = min
                        if max:
                            params['max'] = max
                        if length:
                            params['length'] = length
                        data_dict[col['name']].append(genString(**params))
                    elif col['type'] == 'boolean':
                        data_dict[col['name']].append(genBool())
                    elif col['type'].startswith('decimal'):
                        # Pass precision and scale to genDecimal
                        precision = col.get('precision')  # Default precision
                        scale = col.get('scale')  # Default scale
                        min_value = col.get('min')  # Default min
                        max_value = col.get('max')  # Default max
                        params = {}
                        if precision:
                            params['precision'] = precision
                        if scale:
                            params['scale'] = scale    
                        if min:
                            params['min'] = min_value
                        if max:
                            params['max'] = max_value
                        
                        # Generate a decimal value
                        data_dict[col['name']].append(genDecimal(**params))
                    
        else:
            data_settings[key] = values
            # Handle other settings if needed
            
    # Convert the dictionary to a DataFrame
    data = pd.DataFrame(data_dict) if isinstance(type_dataframe, pd.DataFrame) else pl.DataFrame(data_dict)
    
    # Assert the DataFrame is not empty
    assert isinstance(data, pl.DataFrame) or isinstance(data, pd.DataFrame)
    assert data.shape[0] == nb_rows  # Ensure nb_rows rows are generated
    assert len([col['name'] for col in data_model['columns'] if col['name'] in data.columns]) == len(data.columns)  # Ensure expected columns exist
    
    return data, data_settings