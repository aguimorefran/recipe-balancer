const config = {
  isDocker: process.env.DOCKER_APP === "true",
  requests: {
    docker: "backend:8000",
    local: "http://127.0.0.1:8000",
  },
  getRequestUrl: function () {
    return this.isDocker ? this.requests.docker : this.requests.local;
  },
};

export default config;
