/**
 * @file handprotocol.h
 * @brief DexHand灵巧手协议接口
 * -
 * 本文件定义了DexHand灵巧手协议接口类。该类提供了以下功能:
 * - 解析数据
 * - 打包数据
 * -
 * @author Fourier
 * @date 2025-02-28
 * @copyright Copyright (c) 2025 Fourier. All rights reserved.
 */

#ifndef __HANDPROTOCOL_H__
#define __HANDPROTOCOL_H__

#include <vector>

class HandProtocol
{
    public:
    static int ParseErrorCodes(const char* data, int size, std::vector<long>& fdb);
};

#endif /* __HANDPROTOCOL_H__ */

