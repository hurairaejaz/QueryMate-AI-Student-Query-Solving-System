class QueryRequest {
  final String queryText;
  final String departmentKey;

  QueryRequest({
    required this.queryText,
    this.departmentKey = "software_engineering",
  });

  Map<String, dynamic> toJson() {
    return {
      "query_text": queryText,
      "department_key": departmentKey,
    };
  }
}