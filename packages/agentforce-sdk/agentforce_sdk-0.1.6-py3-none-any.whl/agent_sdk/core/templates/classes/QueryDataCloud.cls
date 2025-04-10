public with sharing class QueryDataCloud {
  // Method to query DataCloud
  @InvocableMethod(label='queryDataCloud')
  public static List<String> queryDataCloud(List<QueryRequest> requests) {
    QueryRequest request = requests[0];
    String query = request.query;
    String mode = request.mode;
    String companyUrl = 'Company_Site';

    List<String> response = new List<String>();
    String result = 'Sorry, I was not able to find any information. Please try again later.';

    if (String.isBlank(query)) {
      query = 'Tell me about your company';
    }

    if (String.isBlank(mode)) {
      mode = 'smart';
    }

    try {
      HttpRequest req = new HttpRequest();
      req.setEndpoint(
        'https://epic-df-demo-ig42q.5sc6y6-4.usa-e2.cloudhub.io/v1/api/atlas-generation'
      );
      req.setMethod('POST');
      req.setTimeout(60000);
      req.setHeader('Content-Type', 'application/json');

      // Set the body of the request using the input from the flow
      String body =
        '{"Query": "' +
        query +
        '", "GenerationMode": "' +
        mode +
        '", "CompanyUrl": "' +
        companyUrl +
        '"}';
      req.setBody(body);

      // Send the HTTP request
      Http http = new Http();
      HttpResponse httpResponse = http.send(req);

      // Set the response data
      result = httpResponse.getBody();
    } catch (Exception e) {
    }

    response.add(result);
    return response;
  }

  public with sharing class QueryRequest {
    @InvocableVariable(required=true)
    public String query;
    @InvocableVariable(required=false)
    public String mode;
  }
}
