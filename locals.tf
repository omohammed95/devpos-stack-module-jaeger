locals {
  helm_values = [{
    allInOne = {
      ingress = {
        enabled = true
        annotations = {
          "cert-manager.io/cluster-issuer"                   = "${var.cluster_issuer}"
          "traefik.ingress.kubernetes.io/router.entrypoints" = "websecure"
          "traefik.ingress.kubernetes.io/router.middlewares" = "traefik-withclustername@kubernetescrd"
          "traefik.ingress.kubernetes.io/router.tls"         = "true"
          "ingress.kubernetes.io/ssl-redirect"               = "true"
          "kubernetes.io/ingress.allow-http"                 = "false"
        }
        hosts = [
          "jaeger.apps.${var.base_domain}",
          "jaeger.apps.${var.cluster_name}.${var.base_domain}",
        ]
        tls = [{
          secretName = "jaeger-tls"
          hosts = [
            "jaeger.apps.${var.base_domain}",
            "jaeger.apps.${var.cluster_name}.${var.base_domain}",
          ]
        }]
      }
    }
  }]
}
