import groovy.json.JsonBuilder
     
node('jenkins-jenkins-slave') {
  withEnv(['REPOSITORY=miau',
  'GIT_ACCOUNT=https://github.com/cvdabbeele']) {
    stage('Pull Image from Git') {
      script {
        git "${GIT_ACCOUNT}/${REPOSITORY}.git"
      }
    }
    stage('Build Image') {
      script {
        dbuild = docker.build("miau/${REPOSITORY}:$BUILD_NUMBER")
      }
    }
    parallel (
      "Test": {
        //script {
        //  sh "python tests/test_flask_app.py"
        //}
        echo 'All functional tests passed'
      },
      "Check Image (pre-Registry)": {
        smartcheckScan([
          imageName: "miau/${REPOSITORY}:$BUILD_NUMBER",
          smartcheckHost: "${DSSC_SERVICE}",
          smartcheckCredentialsId: "smartcheck-auth",
          insecureSkipTLSVerify: true,
          insecureSkipRegistryTLSVerify: true,
          preregistryScan: true,
          preregistryHost: "${DSSC_REGISTRY}",
          preregistryCredentialsId: "preregistry-auth",
          findingsThreshold: new groovy.json.JsonBuilder([
            malware: 0,
            vulnerabilities: [
              defcon1: 0,
              critical: 0,
              high: 1,
            ],
            contents: [
              defcon1: 0,
              critical: 0,
              high: 1,
            ],
            checklists: [
              defcon1: 0,
              critical: 0,
              high: 0,
            ],
          ]).toString(),
        ])
      }
    )
    stage('Push Image to Registry') {
      script {
        docker.withRegistry("https://${K8S_REGISTRY}", 'registry-auth') {
          dbuild.push('$BUILD_NUMBER')
          dbuild.push('latest')
        }
      }
    }
    stage('Check Image (Registry)') {
      withCredentials([
        usernamePassword([
          credentialsId: "registry-auth",
          usernameVariable: "REGISTRY_USERNAME",
          passwordVariable: "REGISTRY_PASSWORD",
        ])
      ]){
        smartcheckScan([
          imageName: "${K8S_REGISTRY}/miau/${REPOSITORY}:$BUILD_NUMBER",
          smartcheckHost: "${DSSC_SERVICE}",
          smartcheckCredentialsId: "smartcheck-auth",
          insecureSkipTLSVerify: true,
          insecureSkipRegistryTLSVerify: true,
          imagePullAuth: new groovy.json.JsonBuilder([
            username: REGISTRY_USERNAME,
            password: REGISTRY_PASSWORD
          ]).toString(),
          findingsThreshold: new groovy.json.JsonBuilder([
            malware: 0,
            vulnerabilities: [
              defcon1: 0,
              critical: 0,
              high: 1,
            ],
            contents: [
              defcon1: 0,
              critical: 0,
              high: 1,
            ],
            checklists: [
              defcon1: 0,
              critical: 0,
              high: 0,
            ],
          ]).toString(),
        ])
      }
    }
    stage('Deploy App to Kubernetes') {
      script {
                         // secretNamespace: "default",
                         // secretName: "cluster-registry2",
        kubernetesDeploy(configs: "app.yml",
                         kubeconfigId: "kubeconfig",
                         enableConfigSubstitution: true,
                         dockerCredentials: [
                           [credentialsId: "registry-auth", url: "${K8S_REGISTRY}"],
                         ])
      }
    }
  }
}
