# Cloud infra eindopdracht (Frog DNS)

Dynamic DNS service based on cloud principles. Service principles are basically Duck DNS but with our own DNS environment. Made with another student of HU.
The service is currently offline. (Because Azure is expensive AF and no one uses this)

> Small demo video : https://jmp.sh/YNGH0X9 More UI below.

> Note: has 192.168.37.100 and 127.0.0.1 Ips whitelisted for Google Auth

## Uses
- Google Oauth2 - Authentication 
- Mongo Atlass - Persistence
- Azure App Service - Automation & Measurement
- Sentry - Monitoring
- Github - Version management, Container Registry & Automations
- AWS - Terraform example & tinkering
- Openstack - Tinkering, leren van cloud principes


### Specs
- Google Oauth (gebruik gemaakt van nip.io)
- Automations en CI via Azure App service
- Zowel REST als UI interfaces. Record CRUD is 100% REST
- Ook werkend via k8s deployment (wel op localhost, beter voor elasticity)
- Authentication via UUID hex token zowel UI via cookie als Rest via Header.
- Persistence via PyMongo & GUI
- Containerized via Docker image geupload naar ghcr.io, gebruikt in k8s deployment

## Automations
Runs deployment on every commit on the `master` branch. Automations are made with Associated Github Actions. This application runs on Azure App Service and the action code is partly given by Azure. Hosted via Gunicorn

## Images
<a href="https://ibb.co/QcCLbp1"><img src="https://i.ibb.co/sP6nmbM/Screenshot-2021-03-30-at-16-47-08.png" alt="Screenshot-2021-03-30-at-16-47-08" border="0"></a>
<a href="https://ibb.co/5nNZx1x"><img src="https://i.ibb.co/TbVyqwq/Screenshot-2021-03-30-at-16-46-58.png" alt="Screenshot-2021-03-30-at-16-46-58" border="0"></a>
<a href="https://ibb.co/xGs2bHK"><img src="https://i.ibb.co/rMtQhsK/Screenshot-2021-03-30-at-16-45-56.png" alt="Screenshot-2021-03-30-at-16-45-56" border="0"></a>
<a href="https://ibb.co/9tc55zq"><img src="https://i.ibb.co/rsFrrTZ/Screenshot-2021-03-30-at-16-46-02.png" alt="Screenshot-2021-03-30-at-16-46-02" border="0"></a>
<a href="https://ibb.co/tHMfhvr"><img src="https://i.ibb.co/2F726C4/Screenshot-2021-03-30-at-16-46-10.png" alt="Screenshot-2021-03-30-at-16-46-10" border="0"></a>

## Monitoring via Sentry
<a href="https://ibb.co/3TWtF0Y"><img src="https://i.ibb.co/HKYmPrp/Screenshot-2021-03-30-at-17-19-35.png" alt="Screenshot-2021-03-30-at-17-19-35" border="0"></a>

## Microk8s example

```bash
microk8s kubectl apply -f k8s.yml
```

To get more info use:
```bash
microk8s kubectl get all -o wide
```

Response
```bash
~/code/cloud-infra-eindopdracht(master*) » mctl get all -o wide
NAME                                               READY   STATUS    RESTARTS   AGE   IP             NODE          NOMINATED NODE   READINESS GATES
pod/cim-eindopdracht-deployment-67db79454d-2bf6k   1/1     Running   0          52m   10.1.254.101   microk8s-vm   <none>           <none>

NAME                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE   SELECTOR
service/kubernetes             ClusterIP   10.152.183.1     <none>        443/TCP          8d    <none>
service/cim-eindopdracht-svc   NodePort    10.152.183.236   <none>        5000:30000/TCP   52m   app=cim-eindopdracht

NAME                                          READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS         IMAGES                                                SELECTOR
deployment.apps/cim-eindopdracht-deployment   1/1     1            1           52m   cim-eindopdracht   ghcr.io/noudadrichem/cloud-infra-eindopracht:latest   app=cim-eindopdracht

NAME                                                     DESIRED   CURRENT   READY   AGE   CONTAINERS         IMAGES                                                SELECTOR
replicaset.apps/cim-eindopdracht-deployment-67db79454d   1         1         1       52m   cim-eindopdracht   ghcr.io/noudadrichem/cloud-infra-eindopracht:latest   app=cim-eindopdracht,pod-template-hash=67db79454d
```
