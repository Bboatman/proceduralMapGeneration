#include "edge.h"
#include "graph.h"
#include "math.h"
#include "scoped_ptr.h"

#include <iostream>

#define NUM_SEGMENTS  4

#define DT (1.0/60)

Graph* CreateGraph() {
  Graph* graph = new Graph();

  int N;
  std::cin >> N;
  std::cout << "Reading " << N << " edges\n";
  for (int i = 0; i < N; ++i) {
    double a0, z0, a1, z1;
    std::cin >> a0 >> z0 >> a1 >> z1;
    graph->AddEdge(Edge(Point(a0, z0), Point(a1, z1)));
  }

  graph->Print();

  return graph;
}

int main(int argc, const char* argv[]) {
  scoped_ptr<Graph> graph(CreateGraph());

  graph->Subdivide(NUM_SEGMENTS);

  graph->Print();

  // Run simulation
  bool done = false;
  while (!done) {
    done = graph->Step(DT);
  }

  std::cout << "Done\n";
  graph->Print();

  return 0;
}
