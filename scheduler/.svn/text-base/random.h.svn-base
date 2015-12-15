// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)
// Description: schedule service main

#ifndef SEARCH2_CRAWLER_VER2_SCHEDULER_RANDOM_H_
#define SEARCH2_CRAWLER_VER2_SCHEDULER_RANDOM_H_

#include  <random>
#include  <iterator>

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

template<typename Iter, typename RandomGenerator>
Iter select_randomly(Iter start, Iter end, RandomGenerator& g) {
    std::uniform_int_distribution<> dis(0, std::distance(start, end) - 1);
    std::advance(start, dis(g));
    return start;
}

template<typename Iter>
Iter select_randomly(Iter start, Iter end) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return select_randomly(start, end, gen);
}

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2
#endif

