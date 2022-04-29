node {

   stage('Build Docker') {
       // build the docker image from the source code using the BUILD_ID parameter in image name
         sh "docker build --tag python-docker ."
   }
   stage("run docker container"){
        sh "docker run -d -p 5000:5000 python-docker "
    }
}
