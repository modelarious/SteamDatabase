from Server.ServerProxyObject import ServerProxyObject
from multiprocessing.managers import BaseManager

if __name__ == '__main__':
    class ShareObjectBetweenProcesses(BaseManager):  
        pass
  
    ShareObjectBetweenProcesses.register('ServerProxyObject', ServerProxyObject) 
    shareObjectBetweenProcesses = ShareObjectBetweenProcesses()  
    shareObjectBetweenProcesses.start()  
    serverProxyObject = shareObjectBetweenProcesses.ServerProxyObject()
    print(serverProxyObject)

    from time import sleep
    serverProxyObject.setUpcomingState('factorio')
    sleep(1)
    serverProxyObject.setUpcomingState('satisfactory')
    sleep(3)
    serverProxyObject.setFindingNameActiveState('factorio')
    sleep(3)
    serverProxyObject.setFindingNameActiveState('satisfactory')
    
    shareObjectBetweenProcesses.join()

