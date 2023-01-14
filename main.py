from wifi_manager import WifiManager
import wifi_connect as wc
import status as st

# Say 'Hello'
print('')
print('Welcome to -> Labor Status Box <- (alpha) ...')
print('')

# Connecting to wifi ....
#print('Not connecting ...\n') # Comment out to save time
wc.wifi_connect()

# Labor Status Box Logic
st.get_settings_from_csv()
st.show_settings()
st.test_leds()
st.status_update()
