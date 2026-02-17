variable "domain_name" {
  description = "Apex domain name (e.g., soboappliancerepair.com)"
  type        = string
}

variable "github_pages_username" {
  description = "GitHub username for Pages (e.g., kylejoshi)"
  type        = string
}

# --- Google Workspace DNS values ---

variable "google_workspace_verification_txt" {
  description = "Google Workspace domain verification TXT record value"
  type        = string
}

variable "google_workspace_mx_records" {
  description = "Google Workspace MX records"
  type = list(object({
    priority = number
    value    = string
  }))
  default = [
    { priority = 1, value = "ASPMX.L.GOOGLE.COM" },
    { priority = 5, value = "ALT1.ASPMX.L.GOOGLE.COM" },
    { priority = 5, value = "ALT2.ASPMX.L.GOOGLE.COM" },
    { priority = 10, value = "ALT3.ASPMX.L.GOOGLE.COM" },
    { priority = 10, value = "ALT4.ASPMX.L.GOOGLE.COM" },
  ]
}

variable "google_workspace_spf_txt" {
  description = "SPF TXT record value for Google Workspace"
  type        = string
  default     = "v=spf1 include:_spf.google.com ~all"
}

variable "dmarc_txt" {
  description = "DMARC TXT record value"
  type        = string
  default     = "v=DMARC1; p=quarantine"
}

# --- Google Search Console ---

variable "google_site_verification_txt" {
  description = "Google Search Console site verification TXT record value"
  type        = string
}
