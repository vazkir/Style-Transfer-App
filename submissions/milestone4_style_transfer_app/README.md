Milstone 4 - Style Transfer App
==============================
Harvard AC215


## Final presentation link
https://youtu.be/7fQYx9zeyoE



## Notebooks used

Inside [the notebooks](https://github.com/vazkir/Style-Transfer-App/tree/main/notebooks/psp) folder you can find the PSP folder which contains the notebooks we used in colab to:
- Run the original pytorch models
- Convert the pytoch models to ONNX format
- Run the onnx_tf models as tensorflow models

Do note that they have originally been ran in the cloud where have access to other specific PSP folders on where we have pytorch and other tools installed. 

If you want to actually run the notebooks, then please let use know so we can give you access to them.




## PSP API Service

[This folder](https://github.com/vazkir/Style-Transfer-App/tree/main/psp-api-service) contains the api we created that can do the following:
1) Load onnx_tf models into memory
2) Receive an input image as request which is then converted by our first model called 'psp.onnx' to a latent representation of the image which is returned
3) Receive a latent vector which is then mutated to aplpy an age vector. This mutated vector is then used as input and then run through our second "decoder.onnx" model to generate an image with this mutatation
  - For now we have hardcoded to use the age vector to create an older version of the person in the image


## React Frontend

[This contains](https://github.com/vazkir/Style-Transfer-App/tree/main/frontend-react) all our frontend code which leverages the api when an image gets uploaded. Then it gets a latent matched image back from the API. From which the user can then choose to apply an age vector to, to make the current image of a person look older



## Room for improvement


### Model load and inference time
Loading our models into memory already takes more then 2 minutes and gettingt the latent image match from the input image takes more than 10 minutes (!?). As you can notice, this is not optimal for the user experience at all. 

We want to therefore debug our models further in terms of the onnx conversion, since the pytorch model seemed to run way faster. 

### Changing other feature dimensions
Also currently the changing of the image is hardcoded to only change the age vector, while we alreay have the code inplace (which is also tested) to change other dimensions, like eye or gender.

We are planning to implement sliders in the frontend ASAP so the user has more control over how he or she wants to change the image


### Neural Style Transfer
We locally ran notebooks to apply NST, which weren't that fast since the model itself had to train. We have been reading the latest papaers regarding faster style transfer and have found some pre-trained models that can achieve NST within seconds.

We are also planning to get this functionality (besides changing the image in the latent space) to the application as soon as possible.



## Screenshots of our application running

![image description](main_screen.png)
![image description](latent_manipulation.png)
![image description](style_manipulation.png)




## Deployement instructions


### API's to enable in GCP for Project
Search for each of these in the GCP search bar and click enable to enable these API's
* Compute Engine API
* Service Usage API
* Cloud Resource Manager API
* Google Container Registry API
* Kubernetes Engine API

### Start Deployment Docker Container
- Make sure you are in the root directory
-  `cd deployment`
- Run `sh docker-shell.sh` or `docker-shell.bat` for windows
- Check versions of tools
`gcloud --version`
`kubectl version`
`kubectl version --client`

- Check if make sure you are authenticated to GCP
- Run `gcloud auth list`

### Build and Push Docker Containers to GCR
**This step is only required if you have NOT already done this**
```
ansible-playbook deploy-docker-images.yml -i inventory.yml
```

### Create & Deploy Cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
```

### If you want to shell into a container in a Pod
```
kubectl get pods --namespace=mushroom-app-cluster-namespace
kubectl get pod api-5d4878c545-47754 --namespace=mushroom-app-cluster-namespace
kubectl exec --stdin --tty api-5d4878c545-47754 --namespace=mushroom-app-cluster-namespace  -- /bin/bash
```

### View the App
* Copy the `nginx_ingress_ip` from the terminal from the create cluster command
* Go to `http://<YOUR INGRESS IP>.sslip.io`

### Delete Cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=absent
```


## A screenshot of our Kuberneters cluster

![image description](k8_cluster2.png)
![image description](k8_cluster.png)




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
