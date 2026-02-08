variable "domain_name" {
  description = "Apex domain name (e.g., soboappliancerepair.com)"
  type        = string
}

variable "github_pages_username" {
  description = "GitHub username for Pages (e.g., kylejoshi)"
  type        = string
}

# --- Protonmail DNS values ---

variable "protonmail_verification_txt" {
  description = "Protonmail domain verification TXT record value"
  type        = string
}

variable "protonmail_mx_records" {
  description = "Protonmail MX records"
  type = list(object({
    priority = number
    value    = string
  }))
  default = [
    { priority = 10, value = "mail.protonmail.ch" },
    { priority = 20, value = "mailsec.protonmail.ch" },
  ]
}

variable "protonmail_spf_txt" {
  description = "SPF TXT record value for Protonmail"
  type        = string
  default     = "v=spf1 include:_spf.protonmail.ch ~all"
}

variable "protonmail_dkim_cnames" {
  description = "Protonmail DKIM CNAME records: map of selector name to CNAME target"
  type        = map(string)
  default     = {}
}

variable "protonmail_dmarc_txt" {
  description = "DMARC TXT record value"
  type        = string
  default     = "v=DMARC1; p=quarantine"
}

# --- Google ---

variable "google_site_verification_txt" {
  description = "Google Search Console site verification TXT record value"
  type        = string
}
