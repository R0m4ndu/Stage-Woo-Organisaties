import json
import os

def create_org_social_media(Organisatie, dict_list):
    ### Because the gathering of (social) media might take a while create a separate dict just for this.
    if os.path.exists(f"Social_Media_{Organisatie}.json"):
    
        with open(f"Social_Media_{Organisatie}.json", "r") as file:
            social_media_dict = json.load(file)
            people_in_dict = list(social_media_dict.keys())
    
    else:
        social_media_dict = dict()
        people_in_dict = []
    
    for p in dict_list:
        persons_per_func = p['infobox']['foi_dossiers']
        for k, v in persons_per_func.items():
            Identifier = f"{v['foaf_name']} {v['dc_publisher_name']} {v['foi_function']}"
            
            if Identifier not in people_in_dict:
                person_dict = {
                                  'foaf_name': v['foaf_name'],
                                  'foaf_function_type': v['foi_function'],
                                  'dc_publisher_name': v['dc_publisher_name'],
                                  'foaf_firstName': v['foaf_firstName'],
                                  'foaf_lastName': v['foaf_lastName'],
                                  'foaf_initials': v['foaf_initials'],
                                  'website': v['foaf_workplaceHomepage'],
                                  'foi_linkedin': '',
                                  'foi_twitter': '',
                                  'foi_wikipedia': '',
                                  'foaf_workplaceHomepage': '',
                                  'up_to_date': False}
            
                social_media_dict[f"{v['foaf_name']} {v['dc_publisher_name']} {v['foi_function']}"] = person_dict
    
    
    Json = json.dumps(social_media_dict, indent=4)

    # Write JSON string to a text file
    with open(f"Social_Media_{Organisatie}.json", "w") as file:
        file.write(Json)
        
        return 'Done'