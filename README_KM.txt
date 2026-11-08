IT GOLD AI BOT V3 — FREE CLOUD USD NEWS ALERT
============================================

អ្វីដែលវាធ្វើ
- ប្រើ GitHub Actions ជា Cloud job ដោយមិនចាំបាច់បើក Laptop។
- ទាញ USD economic calendar ពី ShowMyTrades Free API (មិនត្រូវការ API key)។
- ពិនិត្យ High និង Medium impact រៀងរាល់ 15 នាទី។
- ផ្ញើ Telegram Alert នៅពេលមាន event ក្នុង 15 នាទីខាងមុខ។
- បើចុច Run workflow ដោយដៃ វាផ្ញើ digest នៃព័ត៌មាន 24 ម៉ោងខាងមុខ។

សំខាន់
- នេះជា Telegram USD News Alert តែប៉ុណ្ណោះ។ វាមិនដំណើរការ MT5, មិនអាន IT_GOLD_DATA.csv,
  មិនបង្កើត XAUUSD market analysis និងមិនបើក/បិទ trade ទេ។
- GitHub schedule គឺ best-effort: ពេលខ្លះអាចយឺត ឬខកខាន run ក្នុងពេល server រវល់។
- មិនមែន VPS បើកជាប់ 24/7 ទេ; វាចាប់ផ្ដើម job ខ្លីៗតាមកាលវិភាគ។
- ដើម្បីប្រើ Actions runner ដោយមិនគិតថ្លៃ សូមដាក់ក្នុង Public GitHub repository។ កូដក្នុង ZIP នេះគ្មាន Token ទេ។
- កុំដាក់ Token ឬ Password ក្នុង code ឬ README។ ដាក់តែ GitHub Actions Secrets ប៉ុណ្ណោះ។

ការតម្លើង
1) បង្កើត GitHub account (បើមិនទាន់មាន) នៅ https://github.com/join
2) បង្កើត New repository ឈ្មោះ it-gold-ai-bot-v3-news ហើយជ្រើស Public។
3) Upload គ្រប់ file និង folder ក្នុង ZIP នេះទៅ root នៃ repository។ ត្រូវរក្សា folder .github/workflows/news-alert.yml។
4) ក្នុង repository ចូល Settings > Secrets and variables > Actions > New repository secret។
5) បង្កើត Secret ទាំងពីរ៖
   - Name: TELEGRAM_BOT_TOKEN  | Value: Token ពី BotFather
   - Name: TELEGRAM_CHAT_IDS   | Value: Telegram numeric user/chat ID។ អាចដាក់ច្រើន ID ដោយបំបែកដោយ comma។
6) ក្នុង Telegram បើក Bot របស់អ្នក ហើយចុច Start ឬផ្ញើ /start ម្ដង។
   សម្រាប់លេខ Chat ID ផ្ទាល់ខ្លួន អាចមើលតាម @userinfobot។
7) នៅ GitHub ចូល Actions > IT GOLD AI BOT V3 - USD News Alert > Run workflow។
8) ពិនិត្យ Telegram។ ការចុច Run workflow ដោយដៃនឹងផ្ញើ digest នៃព័ត៌មាន 24 ម៉ោងខាងមុខ។
9) បន្ទាប់មក workflow នឹងដំណើរការដោយស្វ័យប្រវត្តិរៀងរាល់ 15 នាទី។

ការកំណត់ម៉ោង
Cron: 3,18,33,48 * * * * UTC
ម៉ោងកម្ពុជា (UTC+7): រៀងរាល់ម៉ោងនៅនាទី 10, 25, 40, 55។
GitHub អាចពន្យារពេល schedule នៅពេលមាន load ខ្ពស់។

សុវត្ថិភាព
- មិនត្រូវ paste TELEGRAM_BOT_TOKEN ក្នុង Chat, GitHub code, ឬ screenshot ទេ។
- បើ Token បែកធ្លាយ សូមបង្កើត Token ថ្មីតាម BotFather ភ្លាម។
- Public repository បង្ហាញ source code ប៉ុន្តែ GitHub Actions Secrets មិនបង្ហាញតម្លៃទៅក្នុង code ទេ។

ប្រភព Calendar
https://showmytrades.com/docs/api/economic-calendar
https://showmytrades.com/tools/economic-calendar
