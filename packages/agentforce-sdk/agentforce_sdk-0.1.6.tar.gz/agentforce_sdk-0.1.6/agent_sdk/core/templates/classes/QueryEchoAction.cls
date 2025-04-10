public with sharing class QueryEchoAction {

    // Define input parameters
    public class Input {
        @InvocableVariable(required=true label='query' description='String input for the query.')
        public String query;
        
        @InvocableVariable(required=true label='sample response' description='String input for the expected output that will be echoed back.')
        public String sample_response;
    }

    // Define output parameters
    public class Output {
        @InvocableVariable
        public String echoedOutput;
    }

    // Define the invocable method
    @InvocableMethod(label='Echo Expected Output' description='This action returns the expected output as the result.')
    public static List<Output> echoOutput(List<Input> inputs) {
        // Create a list to store the outputs
        List<Output> results = new List<Output>();

        // Process each input
        for (Input input : inputs) {
            Output output = new Output();
            output.echoedOutput = input.sample_response; // Echo the expected_output
            results.add(output);
        }

        // Return the list of results
        return results;
    }
}