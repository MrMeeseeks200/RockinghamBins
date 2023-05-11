# RockighamBins
Fetch bin day information and property details from rockingham coucil website apis
Note this will only work for Addresses in the City Of Rockingham WA

# Setup
Enter Address into the config.txt file
Run `pip3 install -r requirements.txt` to install dependencies
Ensure you are running python 3

# Running
For a once off run simply run `./runBins.py`
Alternatively to run on a daily schedule run `./scheduledBins.py`

# Output 
A file called output.json will be generated with the latest info for the address provided, this data is also displayed to the console

Example Output
```json
{
    "binday": "Monday",
    "nextRecycleDate": "15 May 2023",
    "isRecycleWeek": true,
    "nextVergeGreenWasteDate": "22 May 2023",
    "isVergeGreenWasteWeek": false,
    "nextVergeGeneralWasteDate": "N/A",
    "isVergeGeneralWasteWeek": false,
    "nextGreenWasteDate": "22 May 2023",
    "isGreenWasteWeek": false,
    "info": {
        "address": "123 Fake Street",
        "suburb": "Rockingham",
        "lot": "Lot 123 on DP 123456",
        "area": "300m²"
    }
}
```
