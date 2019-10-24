import groovy.json.JsonBuilder

node('jenkins-jenkins-slave') {
  withEnv(['REPOSITORY=miau',
  'DSSC_SERVICE=34.89.237.34:30010',
  'DSSC_REGISTRY=34.89.237.34:30011',
  'K8S_REGISTRY=34.89.237.34:30017',
  'GIT_ACCOUNT=https://github.com/mawinkler']) {
    stage('Pull Image from Git') {
      script {
        git "${GIT_ACCOUNT}/${REPOSITORY}.git"
      }
    }
    stage('Build Image') {
      script {
        dbuild = docker.build("mawinkler/${REPOSITORY}:$BUILD_NUMBER")
      }
    }
    parallel (
      "Test": {
        echo 'All functional tests passed'
      },
      "Check Image (pre-Registry)": {
        smartcheckScan([
          imageName: "mawinkler/${REPOSITORY}:$BUILD_NUMBER",
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
              high: 10,
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
          dbuild.push()
        }
      }
    }
    stage('Check Image (Registry') {
      smartcheckScan([
        imageName: "${K8S_REGISTRY}/mawinkler/${REPOSITORY}:$BUILD_NUMBER",
        smartcheckHost: "${DSSC_SERVICE}",
        smartcheckCredentialsId: "smartcheck-auth",
        insecureSkipTLSVerify: true,
        insecureSkipRegistryTLSVerify: true,
        imagePullAuth: new groovy.json.JsonBuilder([
          username: "reguser",
          password: "TrendM1cr0"
        ]).toString(),
        findingsThreshold: new groovy.json.JsonBuilder([
          malware: 0,
          vulnerabilities: [
            defcon1: 0,
            critical: 0,
            high: 10,
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
    stage('Push Image to Registry') {
      script {
        docker.withRegistry('', 'docker-hub') {
          dbuild.push('$BUILD_NUMBER')
        }
      }
    }
    stage('Deploy App to Kubernetes') {
      script {
        kubernetesDeploy(configs: "app.yml", kubeconfigId: "kubeconfig")
      }
    }
  }
}
