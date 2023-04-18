hrefList = ["https://www.google.nl/maps/place/Albert+Heijn+XL+Purmerend/data=!4m7!3m6!1s0x47c606d27286d603:0x855f64e5cc1d569f!8m2!3d52.5100708!4d4.9599204!16s%2Fg%2F1tk223h9!19sChIJA9aGctIGxkcRn1YdzOVkX4U?authuser=0&hl=nl&rclk=1",
"https://www.google.nl/maps/place/Jumbo/data=!4m7!3m6!1s0x47c606b1ec43282b:0xe5230f8b6da24ff2!8m2!3d52.506142!4d4.984732!16s%2Fg%2F1w0h6q63!19sChIJKyhD7LEGxkcR8k-ibYsPI-U?authuser=0&hl=nl&rclk=1",
"https://www.google.nl/maps/place/DekaMarkt+Purmerend/data=!4m7!3m6!1s0x47c606d47760c4ed:0xea280c52de8e6f82!8m2!3d52.5106024!4d4.9530584!16s%2Fg%2F1tdwjq0d!19sChIJ7cRgd9QGxkcRgm-O3lIMKOo?authuser=0&hl=nl&rclk=1",
"https://www.google.nl/maps/place/Vomar+Voordeelmarkt/data=!4m7!3m6!1s0x47c6072169c702b3:0x452086e244ed732f!8m2!3d52.4966362!4d4.9379421!16s%2Fg%2F1tj88mmt!19sChIJswLHaSEHxkcRL3PtROKGIEU?authuser=0&hl=nl&rclk=1",
"https://www.google.nl/maps/place/PLUS+De+Gors/data=!4m7!3m6!1s0x47c606ddb0276f4d:0xb16b490a61e0b0f7!8m2!3d52.4943452!4d4.9531916!16s%2Fg%2F1tgxh7sp!19sChIJTW8nsN0GxkcR97DgYQpJa7E?authuser=0&hl=nl&rclk=1",
"https://www.google.nl/maps/place/PLUS+Ligthart/data=!4m7!3m6!1s0x47c6012e29a8353b:0xab8c77435db08d1f!8m2!3d52.5206841!4d4.9620186!16s%2Fg%2F1tdjqbh_!19sChIJOzWoKS4BxkcRH42wXUN3jKs?authuser=0&hl=nl&rclk=1"
"https://www.google.nl/intl/nl/about/products?tab=lh",
"https://accounts.google.com/ServiceLogin?hl=nl&passive=true&continue=https%3A%2F%2Fwww.google.nl%2Fmaps%2Fsearch%2Fsupermarkt%2Bpurmerend%2F%4052.5072961%2C4.9615036%2C14z%2Fdata%3D!3m1!4b1&service=local&ec=GAZAcQ",
"https://support.google.com/maps/?hl=nl&authuser=0&p=no_javascript"
]


SKIPHREFLIST = ['ServiceLogin?', 'products?', 'no_javascript']


cleanedhrefList = (href for href in hrefList if not any(x for x in SKIPHREFLIST if x in href))

*_, last_href = cleanedhrefList # for a better understanding check PEP 448
print(last_href)


# any(x for x in SKIPHREFLIST if x in java_string)