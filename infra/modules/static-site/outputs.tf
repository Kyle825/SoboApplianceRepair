output "nameservers" {
  description = "Set these nameservers at your domain registrar"
  value       = aws_route53_zone.main.name_servers
}

output "site_url" {
  description = "Live site URL"
  value       = "https://${var.domain_name}"
}
