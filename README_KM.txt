IT TRADE PRO — FREE XAUS GOLD DATA + TELEGRAM ONLY
====================================================

មុខងារក្នុងកំណែនេះ
- ទាញតម្លៃ XAU/USD spot ពី XAUS: https://xaus.com/api/v1/spot?compact=1
- មិនត្រូវការ API Key និងមិនមានថ្លៃប្រចាំខែ ($0)។
- បង្ហាញតម្លៃ USD ក្នុងមួយ troy ounce និងម៉ោងកម្ពុជា (UTC+7)។
- បង្ហាញស្ថានភាពទិន្នន័យពិត៖ FRESH / STALE / UNAVAILABLE។
- បើ XAUS មិនមានតម្លៃពិត នឹងមិនបង្ហាញតម្លៃជំនួស ឬតម្លៃក្លែងក្លាយទេ។
- ផ្ញើតែ Telegram message/signal។ មិនភ្ជាប់ MT5 និងមិនបើក/បិទ Order ដោយស្វ័យប្រវត្តិ។
- រក្សា USD Economic News Alert ដែលមានស្រាប់។

ប្រភព និងថ្លៃសេវា
- XAUS: Free, no API key, fair-use limits. សូមកុំហៅ API លើសចាំបាច់។
- មិនប្រើ Finnhub។
- មិនប្រើ Twelve Data។
- មិនប្រើសេវា API បង់ប្រចាំខែ។
- GoldPrice.dev មិនបានភ្ជាប់ក្នុង build នេះទេ; XAUS ជាប្រភពតែមួយសម្រាប់ XAU/USD។
- តម្លៃ XAUS ជា indicative mid-market spot reference មិនមែន broker bid/ask ឬតម្លៃធានាសម្រាប់ execution ទេ។

ការដំឡើង
1) Upload file និង folder ទាំងអស់ក្នុង ZIP ទៅ GitHub repository (Public ប្រសិនបើប្រើ GitHub Actions Free)។
2) ចូល Settings > Secrets and variables > Actions។
3) បង្កើត Secrets:
   TELEGRAM_BOT_TOKEN = Token ពី Telegram BotFather
   TELEGRAM_CHAT_IDS = Telegram numeric Chat ID (ច្រើន ID បំបែកដោយ comma)
4) បើក Telegram bot ហើយចុច Start ឬផ្ញើ /start។
5) ចូល Actions > IT GOLD AI BOT V3 - USD News Alert > Run workflow ដើម្បីសាកល្បង។
6) ពិនិត្យ Telegram។ Workflow schedule រត់រៀងរាល់ 15 នាទី (GitHub schedule អាចយឺតពេល server រវល់)។

ម៉ោង
- Cron: 3,18,33,48 * * * * UTC
- ម៉ោងកម្ពុជា: ប្រហែលនាទី 10, 25, 40, 55 រៀងរាល់ម៉ោង។
- Timestamp របស់ XAU/USD បម្លែងទៅ Asia/Phnom_Penh (UTC+7)។

ស្ថានភាពទិន្នន័យ
- FRESH: XAUS រាយការណ៍ថាទិន្នន័យថ្មី និងអាយុទិន្នន័យមិនលើស 180 វិនាទី។
- STALE: XAUS ផ្ញើតម្លៃចាស់ពី cache ឬ timestamp ចាស់។ បង្ហាញថាជាតម្លៃចាស់ច្បាស់ៗ។
- UNAVAILABLE: គ្មានតម្លៃពិតដែលអាចប្រើបាន។ មិនបង្កើតលេខតម្លៃ។
- កូដពិនិត្យ data_state និង timestamp មុនបង្ហាញស្ថានភាព។

សុវត្ថិភាព
- កុំដាក់ Telegram Token ក្នុង source code ឬ chat។
- ប្រើ GitHub Actions Secrets ប៉ុណ្ណោះ។
- បើ Token បែកធ្លាយ សូម revoke/create ថ្មីតាម BotFather។

ចំណាំ
- GitHub Actions គឺ scheduled cloud job មិនមែន VPS 24/7។
- Telegram Signal Only មិនមែនសេវាណែនាំទិញ/លក់ និងមិនដាក់ order ជំនួសអ្នកទេ។
- មិនធានាថា GitHub schedule នឹងចេញត្រឹមម៉ោងជាក់លាក់។
