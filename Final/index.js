var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-2'});
var sqs = new AWS.SQS();


console.log('Loading function');

exports.handler = function(event, context)
{
   var date= new Date(Date.now()).toLocaleString('en-US',{timeZone: 'America/Denver'});
   console.log('Received event:', JSON.stringify(event, null, 2));
   console.log('Output =', event.data);

   //Message to be transferred to SQS Queue
   var params = {
    DelaySeconds: 0,
    MessageBody: JSON.stringify(event, null, 2) +" "+ date ,
    QueueUrl: "https://sqs.us-east-2.amazonaws.com/552197220785/MsgQueue.fifo",
    MessageGroupId: 'STRING_VALUE'
   };

   sqs.sendMessage(params, function(err,data)
   {
   if(err) 
      {
        console.log('error:',"Fail Send Message" + err);
        context.done('error',"ERROR Put SQS"); //Error with message
      }
   else
   {
     console.log('data:',data.MessageId);
     context.done(null,''); //SUCCESS
   }
});
   //console.log('value1 =', event.key1);
   //console.log('value2 =', event.key2);
   //console.log('value3 =', event.key3);
   return event.key1;  // Echo back the first key value
   // throw new Error('Something went wrong');
};
