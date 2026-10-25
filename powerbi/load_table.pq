let
    // Change this path. Duplicate per mart if you choose to build an extra native report.
    Source = Csv.Document(File.Contents("C:\CHANGE_ME\fuzzy-factory-analytics\data\exports\fct_orders.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{"order_id",Int64.Type},{"order_date",type date},{"user_id",Int64.Type},{"revenue_usd",Currency.Type},{"cogs_usd",Currency.Type},{"gross_profit_usd",Currency.Type},{"refund_usd",Currency.Type}})
in
    Typed
