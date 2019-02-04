items = [
    {
        'name' : "Joel",
        'school' : "UNMSM"
    },
     {
        'name' : "Joel",
        'school' : "UNI"
    },
    {
        'name': "Rodrigo",
        'school':"UCV"
    }
]

while  next(filter(lambda x : x['name'] == 'Joel', items),None):
    print("HOla")
