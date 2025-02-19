# Setting HTMX Attributes

###  x_get
* This argument specifies the endpoint to call when the input value changes.
```
x_get="/update_events"
```
* Ensure the endpoint matches the actual path precisely, including correct slashes.
* When a user changes a date value, this triggers a GET request to the specified endpoint.

### h_target
* Defines the HTML element to update on the page.
```
hx_target="#event"
```
* In this case, #event is the ID for the <select> HTML element containing the list of event options.
  
* Prefixing the ID with a # symbol tells HTMX "Find the element with this ID"

### hx_include
* Ensures that additional data (like the end date) is sent along with the request.
```
hx_include="#event_end_filter"
```
* This grabs the value entered into the input with the name date_end before sending the request

### hx_swap
* Specifies how the HTML element should be replaced.
```
hx_swap="outerHTML"
```
* Setting hx_swap to "outerHTML" replaces the entire element, not just its content.
