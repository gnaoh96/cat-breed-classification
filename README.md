# **Cat Breed Classification Model** 
## **Overall System Architect**
![System Architect](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/m1_latest_architect.png)

## **Table of Contents**
+ API Example
+ How-to Guide
  + I. Running model locally
    + 1.1 Creating & activating conda environment with python 3.9
    + 1.2 Install prerequisites
    + 1.3 Navigate to app directory
    + 1.4 Connect service app with Uvicorn
    + 1.5 Another way to deploy model locally with Docker Compose
  + II. Model-serving with Google Kubernetes Engine (GKE)
    + Install GCloud Packages
    + 2.1 Create GKE cluster with Terraform (infrastruture as code)
    + 2.2 Connect to GKE cluster with GCloud command
    + 2.3 Switch to your GKE cluster environment (using kubectl)
    + 2.4 Create cluster namespace
    + 2.5 Deploy Nginx Ingress Controller with Helm-chart
    + 2.6 Deploy Cat Breed Classification Application
    + 2.7 Config Domain Name to nginx-ingress's External IP
    + 2.8 Access application at address http://cbp.com/docs
  + III. Tracing with Jaeger & Opentelemetry
    + 3.1 Create Jaeger's namespace & deploy Jaeger application
    + 3.2 Add Jaeger's domain name to nginx's External IP
    + 3.3 Access Jaeger UI - http://cbp.jaeger.com/ & start tracing
  + IV. Monitoring with Prometheus & Grafana (kube-prometheus-stack)
    + 4.1 Create monitoring namespace & deploy kube-prometheus-stack
    + 4.2 Update monitoring domain name to nginx's External IP
    + 4.3 Access Grafana UI & enjoy monitoring dashboards - http://cbp.monitoring.com/grafana
  + V. CI/CD with Jenkins & Google Compute Engine (GCE)
    + 5.1 Create GCE & authentication set-up
    + 5.2 Install & Set-up Jenkins on GCE
    + 5.3 Starting to Build & Deploy automation with Jenkins

## **API Example**
Cat Image to classify:
##
<img src="https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/cat_0.jpg" width="440" height="337">

##
Returned Result  :
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-41-46.png)

## How-to Guide

### 1. Running model locally
#### 1.1 Creating & activating conda environment with python 3.9
```bash
conda create -n my_env python==3.9
conda activate my_env
```

#### 1.2 Install prerequisites
```bash
pip install -r requirements.txt
```

#### 1.3 Navigate to app directory
```bash
cd ./app/
```

#### 1.4 Connect service app with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 30000
```
After that, you can enjoy API at address: http://localhost:30000/docs

![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-43-00.png)

#### 1.5 Another way to deploy model locally with Docker Compose
*** If you already have Docker Engine in your local machine, just execute 1 command:
```bash
docker compose -f docker-compose.yaml up -d
```
---
### 2. Model-serving with Google Kubernetes Engine (GKE)
#### Install GCloud Packages
+ [Install Gcloud CLI](https://cloud.google.com/sdk/docs/install#deb)
+ Install gke-gcloud-auth-plugin:
```bash
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```
+ Setup your GCloud project:
  - Initialize GCloud account:
  ```bash
    gcloud init
    ```
  - Authorize & Login:
  ```bash
    gcloud auth application-default login
    ```
#### 2.1 Create GKE cluster with Terraform (infrastruture as code)
```bash
cd terraform # Navigate to terraform folder
terraform plan # Preview cluster plan
terraform apply # Create cluster
```

#### 2.2 Connect to GKE cluster with GCloud command
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-49-05.png)


#### 2.3 Switch to your GKE cluster environment (using [kubectl](https://kubernetes.io/docs/tasks/tools/))
```bash
kubectx your_gke_cluster
```

#### 2.4 Create cluster namespace
```bash
kubectl create ns nginx-ingress # Nginx Ingress Controller
kubectl create ns model-serving
```

#### 2.5 Deploy Nginx Ingress Controller with [Helm-chart](https://helm.sh/)
```bash
helm upgrade --install nginx-ingress helm-charts/nginx-ingress -n nginx-ingress           
```

#### 2.6 Deploy Cat Breed Classification Application
```bash
helm upgrade --install nginx-ingress helm-charts/model-serving -n model-serving           
```

#### 2.7 Config Domain Name to nginx-ingress's External IP
```bash
kubectl get svc -a # Listing all services & finding your nginx External IP

sudo vim /etc/hosts # Editting hosts_file with Vim
your_nginx_externalIP 

your_nginx-ingress_host cbp.com # Updated content
```

#### 2.8 Access application at above address http://cbp.com/docs
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-52-24.png)

### 3. Tracing with Jaeger & Opentelemetry
#### 3.1 Create Jaeger's namespace & deploy Jaeger application
```bash
kubectl create ns jaeger-tracing

helm upgrade --install jaeger-tracing helm-charts/jaeger-tracing -n jaeger-tracing
```

#### 3.2 Add Jaeger's domain name to nginx's External IP
```bash
sudo vim /ect/hosts

your_nginx-ingress_host cbp.jaeger.com
```

#### 3.3 Access Jaeger UI - http://cbp.jaeger.com/ & start tracing
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-53-32.png)


### 4. Monitoring with Prometheus & Grafana [(kube-prometheus-stack)](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
#### 4.1 Create monitoring namespace & deploy kube-prometheus-stack
```bash
kubectl create ns monitoring

helm upgrade --install -f helm-charts/monitoring/personal_gf_calues.yaml kube-prometheus-stack helm-charts/monitoring/kube-prometheus-stack -n monitoring # Deploy with personal values.yaml to config grafana 
```

#### 4.2 Update monitoring domain name to nginx's External IP
```bash
sudo vim /ect/hosts

your_nginx-ingress_host cbp.monitoring.com
```

#### 4.3 Access Grafana UI & enjoy monitoring dashboards - http://cbp.monitoring.com/grafana
** User: admin; Password: prom-operator
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-54-25.png)


### 5. CI/CD with Jenkins & Google Compute Engine (GCE)
#### 5.1 Create GCE & authentication set-up
+ **Create new Service Account**
  + Navigate to Service Account page, then create a new service account with role as [Compute Admin](https://cloud.google.com/compute/docs/access/iam#compute.admin)
  + After finished, download & save it as json file.
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-55-56.png)

  + Save above json file into ```ansible/secrects``` directory.
  + Update service account's file path in ```ansible/playbook/create_compute_instance.yaml```

+ **Create Google Compute Engine with Ansible**
```bash
ansible-playbook ansible/playbooks/create_compute_instance.yaml
```

+ **Update SSH key**
  + Generate a new SSH key with command: ```ssh-keygen```
  + Config the SSH key on Google Cloud Console at path: ```Setting/Metadata/SSH KEYS```
  + Config ```ansible/inventory``` file with External IP of your Compute Engine Instance & the path to SSH Keys (id_rsa).

#### 5.2 Install & Set-up Jenkins on GCE
+ **Execute this command to deploy Jenkins on your GCE instance**
```bash
ansible-playbook ansible/playbook/deploy_jenkins.yaml
```

+ **Connect to Jenkins UI**
  + Checking Jenkins installed successfully on GCE
    + Access the GCE instance
      ```bash
      ssh -i ~/.ssh/id_rsa YOUR_USERNAME@INSTANCE_EXTERNAL_IP
      ```
    + Verify if Jenkins is running in the Compute Engine instance
      ```bash
      sudo docker ps
      ```
  + Access Jenkins UI via ```INSTANCE_EXTERNAL_IP:8081```
  + Follow the instruction to log in into Jenkins.
  + The password can be retrieved by this way
    ```bash
    # Inside your GCE instance
    sudo docker exec -ti jenkins bash
    cat /var/jenkins_home/secrets/initialAdminPassword
    ```

+ **Connect Jenkins to Github Repo**
  + Add Jenkins to Github Repo Webhook:
    + Payload URL would like ```http://INSTANCE_EXTERNAL_IP:8081//github-webhook/```
    + Event Trigger can be set to: *Pushes* and *Pull Requests*
   ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-57-35.png)


  + Add GitHub Repo to Jenkins:
    + Create new Item - Multibranch Pipeline in Jenkens.
      ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2021-58-27.png)

    + Create new GitHub - Personal Access Token. With this project, we just create a **classic** token.
      ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-02-13.png)

    + Connect Repo to Jenkins with GitHub username, password - Personal Access Token, your repo url. After finished, just click Validate to check connection status.
      ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-02-59.png)


+ **Add DockerHub Token to Jenkins Credential:**
  + Create a new DockerHub Token
  + Copy Token to Jenkins's Credentials
    + Noted: ID must be ```dockerhub``` to match the ```registryCredential``` in Jenkinsfile.
      ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-04-03.png)


+ **Install Jenkins's Plugins**
  + Navigate to ```Manage Jenkins/Plugins``` on Jenkins UI, then select & install list of plugins: **Kubernetes, Docker, Docker Pineline, GCloud SDK Plugins**.
    ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-04-47.png)

  + Restart Jenkins after plugin installation finished
    ```bash
      sudo docker restart jenkins
    ```
    
+ **Setup GKE Connection for Jenkins**
  + Create ```ClusterRoleBinding``` in you GKE instance
    ```bash
    kubectl create clusterrolebinding model-serving-admin-binding \
      --clusterrole=admin \
      --serviceaccount=default:default \
      --namespace=default

    kubectl create clusterrolebinding anonymous-admin-binding \
      --clusterrole=admin \
      --user=system:anonymous \
      --namespace=default
    ```
  + Grant permission for Jenkins to access the GCP Filestore Storage - Config RBAC
    ```bash
    kubectl apply -f k8s/rbac
    ``` 

  + Config Cloud Connection on Jenkins at ```http://INSTANCE_EXTERNAL_IP:8081/manage/configureClouds/```
    + Get ```Kubernetes URL``` & ```Kubernetes server certificate key``` with bash command
    ```bash
      cat ~/.kube/config # if you don't have MiniKF on your machine

      cat ~/minikf-kubeconfig # if you already have MiniKF
    ```

    + Config Jenkins Cloud with ```Kubernetes URL``` as ```Server```, ```Kubernetes server certificate key``` as ```certificate-authority-data```. 
      ![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-05-24.png)

  #### **After all, your Jenkins is ready to use. Let's play around!**


#### 5.3 Starting to Build & Deploy automation with Jenkins
+ You can start manually Build new image & Deploy new version of service application with Trigger Button on Jenkins UI.
+ Another way, when the are changes merged to ```main/ master``` branch, the Pipeline on Jenkins will Run, Build & Deploy new app version from DockerHub to GKE Cluster automatically.
![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-07-54.png)

![image](https://github.com/gnaoh96/cat-breed-classification/blob/main/readme_images/Screenshot%20from%202024-05-14%2022-08-46.png)

---

### **Here is the end of my project, thanks for your viewing!**
### **Kindly give me 1 Github star if you like this project. Thanks youguys once again! <3**
