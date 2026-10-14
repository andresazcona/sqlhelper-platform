output "rollback_alarm_names" {
  description = "Alarms that stop a CodeDeploy release and roll it back."
  value = [
    aws_cloudwatch_metric_alarm.api_5xx.alarm_name,
    aws_cloudwatch_metric_alarm.api_latency.alarm_name,
  ]
}
