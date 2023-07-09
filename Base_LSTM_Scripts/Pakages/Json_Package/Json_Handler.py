import json

ModelCreation={}
ModelRawCreated={}
object_ModelCreation={}


object_ModelCreation={"a":[{"model":"A","mpg":5}]}

#print(object_ModelCreation.get(list(object_ModelCreation.keys())[0])[0])
#### A function must be created using the below line
ModelCreation[list(object_ModelCreation.keys())[0]]=[object_ModelCreation.get(list(object_ModelCreation.keys())[0])[0]]
print(ModelCreation)

"""
object_ModelCreation={"b":[{"model":"B","mpg":10}]}
ModelCreation[object_ModelCreation.keys[0]]=[object_ModelCreation.get(object_ModelCreation.keys[0])]


object_ModelRawCreated={"a":[{"model":"A","mpg":5,"size":50}]}
ModelRawCreated[object_ModelRawCreated.keys[0]]=[object_ModelRawCreated.get(object_ModelRawCreated.keys[0])]
object2_ModelRawCreated={"b":[{"model":"B","mpg":10,"size":100}]}
ModelRawCreated[object_ModelRawCreated.keys[0]]=[object_ModelRawCreated.get(object_ModelRawCreated.keys[0])]


RawModel={ModelCreation,
          ModelRawCreated
}

for i in RawModel.get("ModelCreation"):
  dictionaryLookfor=i.keys()
  print(i.get("a"))
    
object_ModelCreation={"b":[{"model":"B","mpg":10}]}

#### Function must be created ####
ModelCreation[list(object_ModelCreation.keys())[0]]=[object_ModelCreation.get(list(object_ModelCreation.keys())[0])[0]]
print(ModelCreation)