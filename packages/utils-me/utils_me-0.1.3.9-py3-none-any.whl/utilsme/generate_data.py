from utilsme import genInteger, genString, genBool, genDecimal

def generate_dict_data(data_model, nb_rows: int):
    
    data = {}
    data_settings = {}
    
    for key, values in data_model.items():
        if key == 'columns':
            for i in range(nb_rows):
                
                for col in values:
                    if col['name'] not in data.keys():
                        data[col['name']] = []
                    
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
                        data[col['name']].append(genInteger(**params))
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
                        data[col['name']].append(genString(**params))
                    elif col['type'] == 'boolean':
                        data[col['name']].append(genBool())
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
                        data[col['name']].append(genDecimal(**params))
                    
        else:
            data_settings[key] = values
    
    return data