from django.template import Library, Node

register = Library()

@register.simple_tag
def compass(here, there):
    northsouth = there[0] - here[0]
    eastwest = there[1] - here[1]

    if northsouth < 0:
        northsouth_value = "south"
    else:
        northsouth_value = "north"

    if eastwest < 0:
        eastwest_value = "west"
    else:
        eastwest_value = "east"

    northsouth = abs(northsouth)
    eastwest = abs(eastwest)

    if eastwest > 0:
        ratio = northsouth / eastwest
        if ratio < 0.3:
            northsouth_value = " "
    if northsouth_value and northsouth > 0:
        ratio = eastwest / northsouth
        if ratio < 0.3:
            eastwest_value = " "
    
    html_class = "".join(v[0] for v in (northsouth_value,eastwest_value)).lower().strip()
    compass_text = " ".join((northsouth_value,eastwest_value)).strip()
    return '<span class="%s">%s</span>' % (html_class, compass_text)


# south = (52.2379, 0.7438)
# north = (53.2379, 0.7438)
# east = (52.2379, 1.7438)
# west = (52.2379, -1.7438)
# 
# 
# north_west = (52.3009, 0.7172)
# 
# here = (52.2803, 0.7438)
# 
# print compass(here, south)
# print compass(here, north)
# print compass(here, east)
# print compass(here, west)
# print compass(here, north_west)