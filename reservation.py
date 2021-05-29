class Reservation:
    def __init__(self, ddb, table_name):
        self.ddb = ddb
        self.table_name = table_name
    
    def book_table(self, phone_no, time_slot, dining_no):
        response = self.ddb.put_item(
            TableName=self.table_name,
            Item={
                'phone_no': {'S': phone_no},
                'time_slot': {'S': time_slot},
                'dining_no': {'S': dining_no}
            }
        )
        results = {
            'status': 'fail',
            'action': 'book',
        }
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            results['status'] = 'success'
            results['dining_no'] = dining_no
        return results
    
    def cancel_table(self, phone_no):
        response = self.ddb.delete_item(
            TableName=self.table_name,
            Key={'phone_no': {'S': phone_no}}
        )
        results = {
            'status': 'fail',
            'action': 'cancel'
        }
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            results['status'] = 'success'
        return results
