# BunnyBase

BunnyBase is a tool for working with data.
The data won't be stored in a table, they will be stored in categories.

## Performance
__BunnyBase is: time = O(1)__
![][1]
![][2]

## How to install?
You can use PIP to install bunnybase:
`pip install bunnybase`

## Example
```python
from bunnybase import Hub, Data

hub = Hub()
hub << Data('person', firstname='peter', lastname='griffin')
hub << Data('person', firstname='homer', lastname='simpson', favourite_food=['donuts'])
hub << Data('animal', name='cat', age=15)
hub << Data('os', name='linux', rate='good', spyware=False)
hub << Data('distro', name='nixos', good=True)
hub << Data('os', name='windows', free=False, spyware='maybe')

hub.filter(name='cat') # DataList([Data('animal', name='cat', age=15)])
hub.filter('person') # DataList([Data('person', firstname='peter', lastname='griffin'), Data('person', firstname='homer', lastname='simpson', favourite_food=['donuts']), ])
hub.filter(name='*') # DataList([Data('animal', name='cat', age=15), Data('os', name='linux', rate='good', spyware=False), Data('distro', name='nixos', good=True), Data('os', name='windows', free=False, spyware='maybe')])
```



[1]: https://raw.githubusercontent.com/trollmii/bunnybase/master/imgs/adding-data-to-hub.png
[2]: https://raw.githubusercontent.com/trollmii/bunnybase/master/imgs/performance-saving-hub.png