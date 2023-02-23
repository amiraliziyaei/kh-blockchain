import keys
import ast

address = {'131245549234998411433549249498765365756525723273616828178426325418246846747949206629953656092940682656076519844097394443611369353962827560836210498592670432565650120644651923813152129452426525755794152442666943735541129175404209585908117594161175539604071492859947450486798004476079465137989522673826429858499': [5, '65537'], '123780200224713691273337749018347686220071275787969055153324153799739948296558672490908399672652160236599476535516039482556154276212085438128319255987035221925969907274600733728990996196854219783614693892300252278895798243117456813403442532756673101171258079451517165313555164216566297140155899785687104557803': [0, '65537']}
def addaddress(pk,e):
    pk = str(pk)
    e = str(e)
    try :
        address[pk] = address[pk]
    except :
        address[pk] = [0,e]

def checkbalance(pk,amount) :
    pk = str(pk)
    if address[pk][0] >= amount :
        return True
    elif address[pk][0] < amount :
        return False

def plus(pk,amount):
    # Transfer
    pk = str(pk)
    address[pk][0] += amount

def lower(pk,amount):
    # Approve
    pk = str(pk)
    address[pk][0] -= amount

def Transfer(msg,sign,pk):
    # msg = 
    # {from : 0x ,
    # to = 0x ,
    # amount = 0}
    
    if keys.ver(str(msg), str(65537), str(pk), sign) is True:

        if checkbalance(msg['from'], msg['amount']) is True :
            plus(msg['to'], msg['amount'])
            lower(int(msg['from']), int(msg['amount']))
        

msg ={'from' : 131245549234998411433549249498765365756525723273616828178426325418246846747949206629953656092940682656076519844097394443611369353962827560836210498592670432565650120644651923813152129452426525755794152442666943735541129175404209585908117594161175539604071492859947450486798004476079465137989522673826429858499 ,'to' : 123780200224713691273337749018347686220071275787969055153324153799739948296558672490908399672652160236599476535516039482556154276212085438128319255987035221925969907274600733728990996196854219783614693892300252278895798243117456813403442532756673101171258079451517165313555164216566297140155899785687104557803 ,'amount' : 1}

Transfer(msg, keys.sig(str(msg), 15753591300442727063216429973633790831495332440177407859157280450778015776473479621504347706717089279552404647048112568330391031370807070926622364270247978661422033249139791920564731065263104299094073491051605934624266613399361637618577277554534659169756233356202417951707715959700144722074187582348871840673, 131245549234998411433549249498765365756525723273616828178426325418246846747949206629953656092940682656076519844097394443611369353962827560836210498592670432565650120644651923813152129452426525755794152442666943735541129175404209585908117594161175539604071492859947450486798004476079465137989522673826429858499), 131245549234998411433549249498765365756525723273616828178426325418246846747949206629953656092940682656076519844097394443611369353962827560836210498592670432565650120644651923813152129452426525755794152442666943735541129175404209585908117594161175539604071492859947450486798004476079465137989522673826429858499)
print(address)