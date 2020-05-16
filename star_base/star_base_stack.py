from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_cloudfront as cf,
    core
)


# noinspection PyShadowingBuiltins,PyShadowingBuiltins
class StarBaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        table = ddb.Table(self, 'WeatherData',
                          partition_key={'name': 'date_part', 'type': ddb.AttributeType.NUMBER},
                          sort_key={'name': 'time_part', 'type': ddb.AttributeType.NUMBER},
                          read_capacity=1, write_capacity=1)
        main_lambda = _lambda.Function(self, 'MainHandler', runtime=_lambda.Runtime.PYTHON_3_8,
                                       code=_lambda.Code.asset('lambda'),
                                       handler='main.handler',
                                       environment={
                                           'WEATHERDATA_TABLE_NAME': table.table_name
                                       })
        table.grant_read_write_data(main_lambda)
        api = apigw.LambdaRestApi(self, 'MainEndpoint', handler=main_lambda)
        api.add_usage_plan('UsagePlan',
                           throttle=apigw.ThrottleSettings(
                               rate_limit=10,
                               burst_limit=10
                           ))
        cloud_front = cf.CloudFrontWebDistribution(self,
                                                   'Https2HttpDistribution',
                                                   viewer_protocol_policy=cf.ViewerProtocolPolicy.ALLOW_ALL,
                                                   geo_restriction=cf.GeoRestriction.whitelist('US'),
                                                   origin_configs=[
                                                       cf.SourceConfiguration(
                                                           custom_origin_source=cf.CustomOriginConfig(
                                                               domain_name=api.url.lstrip("https://").split("/")[0],
                                                               origin_protocol_policy=cf.OriginProtocolPolicy.HTTPS_ONLY,
                                                           ),
                                                           origin_path='/prod',
                                                           behaviors=[
                                                               cf.Behavior(
                                                                   is_default_behavior=True,
                                                                   allowed_methods=cf.CloudFrontAllowedMethods.ALL,
                                                                   cached_methods=cf.CloudFrontAllowedCachedMethods.GET_HEAD,
                                                                   compress=True,
                                                                   forwarded_values=cf.CfnDistribution.ForwardedValuesProperty(
                                                                       query_string=True,
                                                                   )
                                                               ),
                                                           ],
                                                       )
                                                   ]
                                                   )
        core.CfnOutput(self,
                       'HttpEndpointDomain',
                       value=f'http://{cloud_front.domain_name}',
                       description='CloudFront domain name that accepts requests both in HTTP and HTTPS protocols.',
                       export_name='HTTP-Endpoint')
