
# API Reference
## Reservation
### Endpoint URL
`還沒定好`

### JSON body parameters
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| phone_no | str | required | 訂位/取消的手機號碼
| action | str | required | 'book': 訂位 ; <br> 'cancel': 取消
| time_slot | str | optional | 0: 13:00 ~ 14:00 ;<br>1: 14:00 ~ 15:00 ;<br>2: 15:00 ~ 16:00 ;<br>3: 16:00 ~ 17:00
<br>

### Example response
```json
{
    'status': 'success',
    'action': 'book',
    'dining_id': 'b0001'
}
```

### Response fields
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| status | str | required | 'success' or 'fail'
| action | str | required | 'book' or 'cancel'
| dining_id | str | optional | status = 'success' 且 action = 'book' 時才有
<br>

## Take a Number
### Endpoint URL
`還沒定好`

### JSON body parameters
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| action | str | required | 'line-up': 現場排隊 ;<br>'show-up': 訂位報到
| phone_no | str | optional | 訂位者的手機號碼
<br>

### Example response
```json
{
    'status': 'success',
    'action': 'show-up',
    'dining_no': 'b0001',
    'table_no': '1'
}
```

### Response fields
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| status | str | required | 'success' or 'fail'<br>只有在訂位者提早報到的時候才會 'fail'。
| dining_no | str | required | 用餐號碼。訂位的用餐號碼第一個字母都是 'b'，現場排隊都是全數字。
| table_no | str | optional | 訂位報到成功或者排隊的當下有空桌子，就會回傳桌號。
<br>

## Free a Table
### Endpoint URL
`還沒定好`

### JSON body parameters
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| table_no | str | required | 空出來的桌號
<br>

### Example response
```json
{
    'status': 'success',
    'table_no': '1',
    'occupation': 'booked'
}
```

### Response fields
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| status | str | required | 可以先假設只會有 'success'
| table_no | str | required | 空出來的桌號
| occupation | str | required | 桌子的分配情況<br>'booked' 代表接下來有人訂位 ;<br>'empty' 代表沒有人要用餐 ;<br>除此之外就是用餐號碼

## Table Status
### Endpoint URL
`還沒定好`

### JSON body parameters
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| table_no | str | required | 要查狀態的桌號 |
<br>

### Example response
```json
{
    'status': 'success',
    'table_no': '0',
    'state': 'empty',
    'remain_minutes': 59,
    'remain_seconds': 59
}
```

### Response fields
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| status | str | required | 可以先假設只會有 'success'
| table_no | str | required | 空出來的桌號
| state | str | required | 桌子的分配情況<br>'booked' 代表接下來有人訂位 ;<br>'empty' 代表沒有人要用餐 ;<br>'occupied' 代表有人在用餐
| remain_minutes | number | required | 剩餘分鐘
| remain_seconds | number | required | 剩餘秒數
<br>

## Dining Table
### Endpoint URL
`http://Hackathonbackend-env.eba-ivjdqudb.us-east-1.elasticbeanstalk.com/dining-table`

### JSON body parameters
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| dining_no | str | required | 要查桌號的用餐號碼 |
<br>

### Example response
```json
{
    'status': 'success',
    'dining_no': '001'
    'table_no': '0',
}
```

### Response fields
| Name | Type | Required | Description |
| ---- | ----- | ------ | ---------- |
| status | str | required | success: 有查到桌號 ;<br>fail: 沒查到
| dining_no | str | required | 要查桌號的用餐號碼
| table_no | str | optional | 用餐號碼所在的桌號
<br>
