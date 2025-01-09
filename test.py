if __name__ == "__main__":
    dictionary:list[dict['brand_name': str, 'contents': list[dict['title': str, 'url': str]]]] = [
        {
            'brand_name': 'AMX', 
            'contents': [
                {'title': 'Instructor Led', 'url': 'http://url.com'}
            ]
        }
    ]
    dictionary.append({
        'brand_name': 'JBL'
    })

    contents =  [{'title': 'Online Courses', 'url': 'http://newurl.com'}]

    specific_dict_generator = (entry for entry in dictionary if entry.get('brand_name') == 'JBL')
    specific_dict = specific_dict_generator.send(None)
    specific_dict.update({'contents': contents})
    print(specific_dict)
        
    for entry in dictionary:
        print(entry.get('brand_name'))
        print(entry.get('contents'))