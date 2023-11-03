const config = {
  isDocker: process.env.REACT_APP_DOCKER_APP === "true" ? true : false,
  requests: {
    docker: "http://192.168.1.120:8000",
    local: "http://127.0.0.1:8000",
  },
  getRequestUrl: function () {
    return this.isDocker ? this.requests.docker : this.requests.local;
  },
};

export default config;
