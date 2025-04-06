operations = {
    "get_alerts": {
        "path": "/api/alert/v1/alerts",
        "method": "GET"
    },
    "get_alert": {
        "path": "/api/alert/v1/alerts/{alert_id}",
        "method": "GET"
    },
    "update_alert_status": {
        "path": "/api/alert/v1/alerts/{alert_id}/{action}",
        "method": "PATCH"
    },
    "bulk_update_alerts_status": {
        "path": "/api/alert/v1/alerts/bulk/{action}",
        "method": "PATCH"
    },
    "get_alert_mttr_trend": {
        "path": "/api/alert/v1/report/alerts/mttr/trend",
        "method": "GET"
    },
    "get_alert_mtta_trend": {
        "path": "/api/alert/v1/report/alerts/mtta/trend",
        "method": "GET"
    },
    "get_alert_trend_by_priority": {
        "path": "/api/alert/v1/report/alerts/trend/by/priority",
        "method": "GET"
    },
    "get_pod": {
        "path": "/api/mcm/resource/v1beta1/workload/pods/{name}",
        "method": "GET"
    },
    "get_cluster": {
        "path": "/api/mcm/resource/v1beta1/clusters",
        "method": "GET"
    }
}