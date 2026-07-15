class QueryResponse {
  final int queryId;
  final String status;
  final String? answer;
  final double? confidenceScore;
  final int? matchedKbId;
  final List<Map<String, dynamic>> documents;
  final String message;

  QueryResponse({
    required this.queryId,
    required this.status,
    this.answer,
    this.confidenceScore,
    this.matchedKbId,
    required this.documents,
    required this.message,
  });

  factory QueryResponse.fromJson(Map<String, dynamic> json) {
    return QueryResponse(
      queryId: json["query_id"] ?? 0,
      status: json["status"] ?? "",
      answer: json["answer"],
      confidenceScore: json["confidence_score"] != null
          ? (json["confidence_score"] as num).toDouble()
          : null,
      matchedKbId: json["matched_kb_id"],
      documents: json["documents"] != null
          ? List<Map<String, dynamic>>.from(
        json["documents"].map(
              (x) => Map<String, dynamic>.from(x),
        ),
      )
          : [],
      message: json["message"] ?? "",
    );
  }
}