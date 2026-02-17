# ============================================================
# Hosted Zone
# ============================================================

resource "aws_route53_zone" "main" {
  name = var.domain_name
}

# ============================================================
# GitHub Pages — A records (apex)
# https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
# ============================================================

resource "aws_route53_record" "apex_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"
  ttl     = 3600

  records = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
  ]
}

resource "aws_route53_record" "apex_aaaa" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "AAAA"
  ttl     = 3600

  records = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
  ]
}

# ============================================================
# GitHub Pages — www CNAME
# ============================================================

resource "aws_route53_record" "www_cname" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain_name}"
  type    = "CNAME"
  ttl     = 3600
  records = ["${var.github_pages_username}.github.io"]
}

# ============================================================
# Google Workspace — MX Records
# ============================================================

resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "MX"
  ttl     = 3600

  records = [for mx in var.google_workspace_mx_records : "${mx.priority} ${mx.value}"]
}

# ============================================================
# TXT Records (Google Workspace verification + SPF + Search Console)
# Route53 requires a single TXT recordset per name
# ============================================================

resource "aws_route53_record" "txt" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "TXT"
  ttl     = 3600

  records = [
    var.google_workspace_verification_txt,
    var.google_workspace_spf_txt,
    var.google_site_verification_txt,
  ]
}

# ============================================================
# DMARC TXT Record
# ============================================================

resource "aws_route53_record" "dmarc" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "_dmarc.${var.domain_name}"
  type    = "TXT"
  ttl     = 3600
  records = [var.dmarc_txt]
}
