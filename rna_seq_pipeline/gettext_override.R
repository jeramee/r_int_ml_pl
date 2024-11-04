# gettext_override.R

# Define a custom function to replace gettext functionality.
# This function simply returns the input text,
# acting as a no-operation for localization.
# gettext_override.R in R script
custom_gettext <- function(text) {
  return(text)  # No-operation replacement for translation
}

gettext <- custom_gettext  # Override default gettext
ngettext <- function(single, plural, count) {
  if (count == 1) {
    return(single)
  } else {
    return(plural)
  }
}

message("gettext_override.R has been sourced successfully.")

# In R (gettext_override.R)
suppressWarnings({
  library(gettext)
  message("Warnings suppressed for compatibility.")
})
