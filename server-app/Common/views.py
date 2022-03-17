import json
from django.http import HttpResponse
from .common import *

def get_region_list(request):
    """
    @api {GET} /region_list/ region list
    @apiVersion 0.0.1
    @apiName region_list
    @apiGroup Common
    @apiDescription api to get country or region list

    @apiSuccess (200) {string} region_list String of region list, separated by separator.
    @apiSuccess (200) {string} separator Separator used for splitting region list string.

    @apiSuccessExample {Json} Response-Success
    {
        "region_list": "Afghanistan#Albania#Algeria#Andorra#Angola#Anguilla#Antigua and Barbuda#Arab Emirates#Argentina#Armenia#Aruba#Australia#Austria#Azerbaijan#Bahamas#Bahrain#Bangladesh#Barbados#Belarus#Belgium#Belize#Benin#Bermuda#Bhutan#Bolivia#Bosnia and Herzegovina#Botswana#Bouvet Island#Brazil#Brunei#Bulgaria#Burkina Faso#Burundi#Cambodia#Cameroon#Canada#Cape Verde#Cayman Islands#Central African Republic#Chad#Chile#China, Hong Kong S.A.R.#China, the People's Republic of China (PRC)#Cocos Islands#Colombia#Comoros#Congo#Congo, Democratic Republic of the Congo#Cook Islands#Costa Rica#Croatia#Cuba#Curacao#Cyprus#Czech Republic#Denmark#Djibouti#Dominica#Dominican Republic#Ecuador#Egypt#El Salvador#Equatorial Guinea#Eritrea#Estonia#Ethiopia#Falkland Islands (Malvinas)#Faroe Islands#Fiji#Finland#France#French Guiana#French Polynesia#Gabon#Gambia#Georgia, Republic of Georgia#Germany#Ghana#Gibraltar#Greece#Greenland#Grenada#Guadeloupe#Guatemala#Guernsey#Guinea#Guinea-Bissau#Guyana#Haiti#Honduras#Hungary#Iceland#India#Indonesia#Iran#Iraq#Ireland#Isle of Man#Israel#Italy#Ivory Coast#Jamaica#Japan#Jersey#Jordan#Kazakhstan#Kenya#Kiribati#Kuwait#Kyrgyzstan#Laos#Latvia#Lebanon#Lesotho#Liberia#Libya#Liechtenstein#Lithuania#Luxembourg#Macau#Macedonia (Former Yugoslav Republic)#Madagascar#Malawi#Malaysia#Maldives#Mali#Malta#Marshall Islands#Martinique#Mauritania#Mauritius#Mexico#Moldova, Republic of Moldova#Monaco#Mongolia#Montenegro#Montserrat#Morocco#Mozambique#Myanmar#Namibia#Nauru#Nepal#Netherlands#Netherlands Antilles#New Caledonia#New Zealand#Nicaragua#Niger#Nigeria#Norfolk Island#North Korea#Northern Mariana Islands#Norway#Oman#Pakistan#Palau#Panama#Papua New Guinea#Paraguay#Peru#Philippines#Poland#Portugal#Qatar#Romania#Russian Federation#Rwanda#Saint Helena, Ascension, and Tristan da Cunha#Saint Kitts and Nevis#Samoa#San Marino#Sao Tome and Principe#Saudi Arabia#Senegal#Serbia#Seychelles#Sierra Leone#Singapore#Slovakia#Slovenia#Solomon Islands#Somalia#South Africa#South Georgia and the South Sandwich Islands#South Korea#Spain#Sri Lanka#St. Lucia#St. Vincent and the Grenadines#Sudan#Suriname#Swaziland#Sweden#Switzerland#Syria#Taiwan(Province of China)#Tajikistan#Tanzania#Thailand#Timor-Leste#Togo#Tonga#Trinidad and Tobago#Tunisia#Turkey#Turkmenistan#Turks and Caicos Islands#Tuvalu#Uganda#Ukraine#United Kingdom#United States of America#Uruguay#Uzbekistan#Vanuatu (New Hebrides)#Vatican City State (Holy See)#Venezuela#Viet Nam#Virgin (British) Islands#Western Sahara#Yemen#Yugoslavia#Zambia#Zimbabwe",
        "separator": "#"
    }
    """
    sep = "#"
    response_data = {"region_list": sep.join(sorted(list(REGION2RID.keys()))),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_currency_list(request):
    """
    @api {GET} /currency_list/ currency list
    @apiVersion 0.0.1
    @apiName currency_list
    @apiGroup Common
    @apiDescription api to get currency type list

    @apiSuccess (200) {string} currency_list String of currency type list, separated by separator.
    @apiSuccess (200) {string} separator Separator used for splitting currency type string.

    @apiSuccessExample {Json} Response-Success
    {
        "currency_list": "AED (Emirati Dirham)#AFN (Afghan Afghani)#ALL (Albanian Lek)#AMD (Armenian Dram)#ANG (Dutch Guilder)#AOA (Angolan Kwanza)#ARS (Argentine Peso)#AUD (Australian Dollar)#AWG (Aruban or Dutch Guilder)#AZN (Azerbaijan Manat)#BAM (Bosnian Convertible Mark)#BBD (Barbadian or Bajan Dollar)#BDT (Bangladeshi Taka)#BGN (Bulgarian Lev)#BHD (Bahraini Dinar)#BIF (Burundian Franc)#BMD (Bermudian Dollar)#BND (Bruneian Dollar)#BOB (Bolivian Bolíviano)#BRL (Brazilian Real)#BSD (Bahamian Dollar)#BTN (Bhutanese Ngultrum)#BWP (Botswana Pula)#BYN (Belarusian Ruble)#BZD (Belizean Dollar)#CAD (Canadian Dollar)#CDF (Congolese Franc)#CHF (Swiss Franc)#CLF (Chilean Unidad de Fomento)#CLP (Chilean Peso)#CNH (Chinese Yuan Renminbi Offshore)#CNY (Chinese Yuan Renminbi)#COP (Colombian Peso)#CRC (Costa Rican Colon)#CUC (Cuban Convertible Peso)#CUP (Cuban Peso)#CVE (Cape Verdean Escudo)#CZK (Czech Koruna)#DJF (Djiboutian Franc)#DKK (Danish Krone)#DOP (Dominican Peso)#DZD (Algerian Dinar)#EGP (Egyptian Pound)#ERN (Eritrean Nakfa)#ETB (Ethiopian Birr)#EUR (Euro)#FJD (Fijian Dollar)#FKP (Falkland Island Pound)#GBP (British Pound)#GEL (Georgian Lari)#GGP (Guernsey Pound)#GHS (Ghanaian Cedi)#GIP (Gibraltar Pound)#GMD (Gambian Dalasi)#GNF (Guinean Franc)#GTQ (Guatemalan Quetzal)#GYD (Guyanese Dollar)#HKD (Hong Kong Dollar)#HNL (Honduran Lempira)#HRK (Croatian Kuna)#HTG (Haitian Gourde)#HUF (Hungarian Forint)#IDR (Indonesian Rupiah)#ILS (Israeli Shekel)#IMP (Isle of Man Pound)#INR (Indian Rupee)#IQD (Iraqi Dinar)#IRR (Iranian Rial)#ISK (Icelandic Krona)#JEP (Jersey Pound)#JMD (Jamaican Dollar)#JOD (Jordanian Dinar)#JPY (Japanese Yen)#KES (Kenyan Shilling)#KGS (Kyrgyzstani Som)#KHR (Cambodian Riel)#KMF (Comorian Franc)#KPW (North Korean Won)#KRW (South Korean Won)#KWD (Kuwaiti Dinar)#KYD (Caymanian Dollar)#KZT (Kazakhstani Tenge)#LAK (Lao Kip)#LBP (Lebanese Pound)#LKR (Sri Lankan Rupee)#LRD (Liberian Dollar)#LSL (Basotho Loti)#LYD (Libyan Dinar)#MAD (Moroccan Dirham)#MDL (Moldovan Leu)#MGA (Malagasy Ariary)#MKD (Macedonian Denar)#MMK (Burmese Kyat)#MNT (Mongolian Tughrik)#MOP (Macau Pataca)#MRU (Mauritanian Ouguiya)#MUR (Mauritian Rupee)#MVR (Maldivian Rufiyaa)#MWK (Malawian Kwacha)#MXN (Mexican Peso)#MXV (Unidad de inversión)#MYR (Malaysian Ringgit)#MZN (Mozambican Metical)#NAD (Namibian Dollar)#NGN (Nigerian Naira)#NIO (Nicaraguan Cordoba)#NOK (Norwegian Krone)#NPR (Nepalese Rupee)#NZD (New Zealand Dollar)#OMR (Omani Rial)#PAB (Panamanian Balboa)#PEN (Peruvian Sol)#PGK (Papua New Guinean Kina)#PHP (Philippine Peso)#PKR (Pakistani Rupee)#PLN (Polish Zloty)#PYG (Paraguayan Guarani)#QAR (Qatari Riyal)#RON (Romanian Leu)#RSD (Serbian Dinar)#RUB (Russian Ruble)#RWF (Rwandan Franc)#SAR (Saudi Arabian Riyal)#SBD (Solomon Islander Dollar)#SCR (Seychellois Rupee)#SDG (Sudanese Pound)#SEK (Swedish Krona)#SGD (Singapore Dollar)#SHP (Saint Helenian Pound)#SLL (Sierra Leonean Leone)#SOS (Somali Shilling)#SPL (Seborgan Luigino)#SRD (Surinamese Dollar)#STN (Sao Tomean Dobra)#SVC (Salvadoran Colon)#SYP (Syrian Pound)#SZL (Swazi Lilangeni)#THB (Thai Baht)#TJS (Tajikistani Somoni)#TMT (Turkmenistani Manat)#TND (Tunisian Dinar)#TOP (Tongan Pa'anga)#TRY (Turkish Lira)#TTD (Trinidadian Dollar)#TVD (Tuvaluan Dollar)#TWD (Taiwan New Dollar)#TZS (Tanzanian Shilling)#UAH (Ukrainian Hryvnia)#UGX (Ugandan Shilling)#USD (US Dollar)#UYU (Uruguayan Peso)#UZS (Uzbekistani Som)#VED (Venezuelan Bolívar)#VEF (Venezuelan Bolívar)#VES (Venezuelan Bolívar)#VND (Vietnamese Dong)#VUV (Ni-Vanuatu Vatu)#WST (Samoan Tala)#XAF (Central African CFA Franc BEAC)#XAG (Silver Ounce)#XAU (Gold Ounce)#XBT (Bitcoin)#XCD (East Caribbean Dollar)#XDR (IMF Special Drawing Rights)#XOF (CFA Franc)#XPD (Palladium Ounce)#XPF (CFP Franc)#XPT (Platinum Ounce)#YER (Yemeni Rial)#ZAR (South African Rand)#ZMW (Zambian Kwacha)#ZWD (Zimbabwean Dollar)",
        "separator": "#"
    }
    """
    sep = "#"
    exchange_rate_list = list(CURRENCY2CID.keys())
    exchange_rate_list.sort()
    response_data = {"currency_list": sep.join(exchange_rate_list),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_region2currency(request):
    """
    @api {GET} /region2currency/ region to currency
    @apiVersion 0.0.1
    @apiName region2currency
    @apiGroup Common
    @apiDescription api to get dict region: default currency type

    @apiSuccess (200) {string} region2currency Json with format(region: default currency type).

    @apiSuccessExample {Json} Response-Success
    {
        "region2currency": {
            "Arab Emirates": "AED (Emirati Dirham)",
            "Afghanistan": "AFN (Afghan Afghani)",
            "Albania": "ALL (Albanian Lek)",
            "Armenia": "AMD (Armenian Dram)",
            "Netherlands Antilles": "ANG (Dutch Guilder)",
            "Curacao": "ANG (Dutch Guilder)",
            "Angola": "AOA (Angolan Kwanza)",
            "Argentina": "ARS (Argentine Peso)",
            "Australia": "AUD (Australian Dollar)",
            ...
        }
    }
    """
    response_data = {"region2currency": REGION2CURRENCY}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
