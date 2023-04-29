from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.db import models

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class User(AbstractUser):
    COUNTRY_CHOICES = (
        ("AF", "Afghanistan"),
        ("AX", "Åland Islands"),
        ("AL", "Albania"),
        ("DZ", "Algeria"),
        ("AS", "American Samoa"),
        ("AD", "Andorra"),
        ("AO", "Angola"),
        ("AI", "Anguilla"),
        ("AQ", "Antarctica"),
        ("AG", "Antigua and Barbuda"),
        ("AR", "Argentina"),
        ("AM", "Armenia"),
        ("AW", "Aruba"),
        ("AU", "Australia"),
        ("AT", "Austria"),
        ("AZ", "Azerbaijan"),
        ("BS", "Bahamas"),
        ("BH", "Bahrain"),
        ("BD", "Bangladesh"),
        ("BB", "Barbados"),
        ("BY", "Belarus"),
        ("BE", "Belgium"),
        ("BZ", "Belize"),
        ("BJ", "Benin"),
        ("BM", "Bermuda"),
        ("BT", "Bhutan"),
        ("BO", "Bolivia (Plurinational State of)"),
        ("BQ", "Bonaire, Sint Eustatius and Saba"),
        ("BA", "Bosnia and Herzegovina"),
        ("BW", "Botswana"),
        ("BV", "Bouvet Island"),
        ("BR", "Brazil"),
        ("IO", "British Indian Ocean Territory"),
        ("BN", "Brunei Darussalam"),
        ("BG", "Bulgaria"),
        ("BF", "Burkina Faso"),
        ("BI", "Burundi"),
        ("CV", "Cabo Verde"),
        ("KH", "Cambodia"),
        ("CM", "Cameroon"),
        ("CA", "Canada"),
        ("KY", "Cayman Islands"),
        ("CF", "Central African Republic"),
        ("TD", "Chad"),
        ("CL", "Chile"),
        ("CN", "China"),
        ("CX", "Christmas Island"),
        ("CC", "Cocos (Keeling) Islands"),
        ("CO", "Colombia"),
        ("KM", "Comoros"),
        ("CG", "Congo"),
        ("CD", "Congo (Democratic Republic of the)"),
        ("CK", "Cook Islands"),
        ("CR", "Costa Rica"),
        ("CI", "Côte d'Ivoire"),
        ("HR", "Croatia"),
        ("CU", "Cuba"),
        ("CW", "Curaçao"),
        ("CY", "Cyprus"),
        ("CZ", "Czech Republic"),
        ("DK", "Denmark"),
        ("DJ", "Djibouti"),
        ("DM", "Dominica"),
        ("DO", "Dominican Republic"),
        ("EC", "Ecuador"),
        ("EG", "Egypt"),
        ("SV", "El Salvador"),
        ("GQ", "Equatorial Guinea"),
        ("ER", "Eritrea"),
        ("EE", "Estonia"),
        ("ET", "Ethiopia"),
        ("FK", "Falkland Islands (Malvinas)"),
        ("FO", "Faroe Islands"),
        ("FJ", "Fiji"),
        ("FI", "Finland"),
        ("FR", "France"),
        ("GF", "French Guiana"),
        ("PF", "French Polynesia"),
        ("TF", "French Southern Territories"),
        ("GA", "Gabon"),
        ("GM", "Gambia"),
        ("GE", "Georgia"),
        ("DE", "Germany"),
        ("GH", "Ghana"),
        ("GI", "Gibraltar"),
        ("GR", "Greece"),
        ("GL", "Greenland"),
        ("GD", "Grenada"),
        ("GP", "Guadeloupe"),
        ("GU", "Guam"),
        ("GT", "Guatemala"),
        ("GG", "Guernsey"),
        ("GN", "Guinea"),
        ("GW", "Guinea-Bissau"),
        ("GY", "Guyana"),
        ("HT", "Haiti"),
        ("HM", "Heard Island and McDonald Islands"),
        ("VA", "Holy See"),
        ("HN", "Honduras"),
        ("HK", "Hong Kong"),
        ("HU", "Hungary"),
        ("IS", "Iceland"),
        ("IN", "India"),
        ("ID", "Indonesia"),
        ("IR", "Iran (Islamic Republic of)"),
        ("IQ", "Iraq"),
        ("IE", "Ireland"),
        ("IM", "Isle of Man"),
        ("IL", "Israel"),
        ("IT", "Italy"),
        ("JM", "Jamaica"),
        ("JP", "Japan"),
        ("JE", "Jersey"),
        ("JO", "Jordan"),
        ("KZ", "Kazakhstan"),
        ("KE", "Kenya"),
        ("KI", "Kiribati"),
        ("KP", "Korea (Democratic People's Republic of)"),
        ("KR", "Korea, Republic of"),
        ("KW", "Kuwait"),
        ("KG", "Kyrgyzstan"),
        ("LA", "Lao People's Democratic Republic"),
        ("LV", "Latvia"),
        ("LB", "Lebanon"),
        ("LS", "Lesotho"),
        ("LR", "Liberia"),
        ("LY", "Libya"),
        ("LI", "Liechtenstein"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("MO", "Macao"),
        ("MK", "Macedonia (the former Yugoslav Republic of)"),
        ("MG", "Madagascar"),
        ("MW", "Malawi"),
        ("MY", "Malaysia"),
        ("MV", "Maldives"),
        ("ML", "Mali"),
        ("MT", "Malta"),
        ("MH", "Marshall Islands"),
        ("MQ", "Martinique"),
        ("MR", "Mauritania"),
        ("MU", "Mauritius"),
        ("YT", "Mayotte"),
        ("MX", "Mexico"),
        ("FM", "Micronesia (Federated States of)"),
        ("MD", "Moldova, Republic of"),
        ("MC", "Monaco"),
        ("MN", "Mongolia"),
        ("ME", "Montenegro"),
        ("MS", "Montserrat"),
        ("MA", "Morocco"),
        ("MZ", "Mozambique"),
        ("MM", "Myanmar"),
        ("NA", "Namibia"),
        ("NR", "Nauru"),
        ("NP", "Nepal"),
        ("NL", "Netherlands"),
        ("NC", "New Caledonia"),
        ("NZ", "New Zealand"),
        ("NI", "Nicaragua"),
        ("NE", "Niger"),
        ("NG", "Nigeria"),
        ("NU", "Niue"),
        ("NF", "Norfolk Island"),
        ("MP", "Northern Mariana Islands"),
        ("NO", "Norway"),
        ("OM", "Oman"),
        ("PK", "Pakistan"),
        ("PW", "Palau"),
        ("PS", "Palestine, State of"),
        ("PA", "Panama"),
        ("PG", "Papua New Guinea"),
        ("PY", "Paraguay"),
        ("PE", "Peru"),
        ("PH", "Philippines"),
        ("PN", "Pitcairn"),
        ("PL", "Poland"),
        ("PT", "Portugal"),
        ("PR", "Puerto Rico"),
        ("QA", "Qatar"),
        ("RE", "Réunion"),
        ("RO", "Romania"),
        ("RU", "Russian Federation"),
        ("RW", "Rwanda"),
        ("BL", "Saint Barthélemy"),
        ("SH", "Saint Helena, Ascension and Tristan da Cunha"),
        ("KN", "Saint Kitts and Nevis"),
        ("LC", "Saint Lucia"),
        ("MF", "Saint Martin (French part)"),
        ("PM", "Saint Pierre and Miquelon"),
        ("VC", "Saint Vincent and the Grenadines"),
        ("WS", "Samoa"),
        ("SM", "San Marino"),
        ("ST", "Sao Tome and Principe"),
        ("SA", "Saudi Arabia"),
        ("SN", "Senegal"),
        ("RS", "Serbia"),
        ("SC", "Seychelles"),
        ("SL", "Sierra Leone"),
        ("SG", "Singapore"),
        ("SX", "Sint Maarten (Dutch part)"),
        ("SK", "Slovakia"),
        ("SI", "Slovenia"),
        ("SB", "Solomon Islands"),
        ("SO", "Somalia"),
        ("ZA", "South Africa"),
        ("GS", "South Georgia and the South Sandwich Islands"),
        ("SS", "South Sudan"),
        ("ES", "Spain"),
        ("LK", "Sri Lanka"),
        ("SD", "Sudan"),
        ("SR", "Suriname"),
        ("SJ", "Svalbard and Jan Mayen"),
        ("SZ", "Swaziland"),
        ("SE", "Sweden"),
        ("CH", "Switzerland"),
        ("SY", "Syrian Arab Republic"),
        ("TW", "Taiwan, Province of China"),
        ("TJ", "Tajikistan"),
        ("TZ", "Tanzania, United Republic of"),
        ("TH", "Thailand"),
        ("TL", "Timor-Leste"),
        ("TG", "Togo"),
        ("TK", "Tokelau"),
        ("TO", "Tonga"),
        ("TT", "Trinidad and Tobago"),
        ("TN", "Tunisia"),
        ("TR", "Turkey"),
        ("TM", "Turkmenistan"),
        ("TC", "Turks and Caicos"),
        ("TV", "Tuvalu"),
        ("UG", "Uganda"),
        ("UA", "Ukraine"),
        ("AE", "United Arab Emirates"),
        ("GB", "United Kingdom of Great Britain and Northern Ireland"),
        ("UM", "United States Minor Outlying Islands"),
        ("US", "selected>United States of America"),
        ("UY", "Uruguay"),
        ("UZ", "Uzbekistan"),
        ("VU", "Vanuatu"),
        ("VE", "Venezuela (Bolivarian Republic of)"),
        ("VN", "Viet Nam"),
        ("VG", "Virgin Islands (British)"),
        ("VI", "Virgin Islands (U.S.)"),
        ("WF", "Wallis and Futuna"),
        ("EH", "Western Sahara"),
        ("YE", "Yemen"),
        ("ZM", "Zambia"),
        ("ZW", "Zimbabwe"),
    )
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


class Course(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('upcoming', 'Upcoming'),
    )
    DIFFICULTY_LEVELS = (
        ('introductory', 'Introductory'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    price = models.IntegerField() # cents    
    is_free = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)

    what_you_will_learn = models.TextField(blank=True)
    course_language = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    instructor = models.ManyToManyField(Instructor, related_name='courses')

    def __str__(self):
        return self.title
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Enroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now)
    certificate = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.user.username}'s cart"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent_off = models.PositiveIntegerField()
    duration = models.CharField(max_length=50, choices=[('once', 'Once'), ('forever', 'Forever')], default='once')
    duration_in_months = models.PositiveIntegerField(blank=True, null=True)
    redeem_by = models.DateTimeField(blank=True, null=True)
        
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
