# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'listeners'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'project'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'external_access'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'envoy_translator_ui.content.listeners.panel.ListenerPanel'
