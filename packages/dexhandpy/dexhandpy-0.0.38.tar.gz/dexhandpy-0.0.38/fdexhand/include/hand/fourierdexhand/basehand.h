#ifndef __BASEHAND_H__
#define __BASEHAND_H__

#include <iostream>
#include <memory>
#include <chrono>
#include <cstring>
#include <vector>
#include "./../rapidjson/stringbuffer.h"
#include "./../rapidjson/writer.h"
#include "./../rapidjson/document.h"
#include "./../rapidjson/rapidjson.h"
#include "./../commsocket/commsocket.h"

using namespace CommSocket;

#define BROADCAST_ADDR "192.168.137.255"
#define LEFT_DEFAULT_ADDR "192.168.137.19"
#define RIGHT_DEFAULT_ADDR "192.168.137.39"

#define CTROLLER_PORT 2333
#define COMMUNICATION_PORT 2334
#define FAST_BYTE_PORT 2335

#define INSPIRE_NAME "FSH"
#define DEXHAND_FDH6 "fdhv1"
#define DEXHAND_FDH12 "fdhv2"

#define DEXHAND_TYPE_6L "FDH-6L"
#define DEXHAND_TYPE_6R "FDH-6R"

#define DEXHAND_TYPE_12L "FDH-12L"
#define DEXHAND_TYPE_12R "FDH-12R"

#define INSPIRE_TYPE "Hand"

namespace BaseHandProtocol
{
    typedef enum 
    {
        SUCCESS = 0,
        FAIL = -1,
        TIMEOUT = -2
    } FdhReturnCode;
    class BaseHand
    {
    public:
        std::shared_ptr<Transmit::UDPSocket> ctrl_udp_socket;
        std::shared_ptr<Transmit::UDPSocket> comm_udp_socket;
        std::shared_ptr<Transmit::UDPSocket> fast_udp_socket;

    protected:
        std::vector<float> position_;
        std::vector<float> velocity_;
        std::vector<float> current_;

    public:
        virtual ~BaseHand() = default;

        virtual FdhReturnCode calibration() = 0;
        virtual FdhReturnCode enable() = 0;
        virtual FdhReturnCode disable() = 0;
        virtual FdhReturnCode reboot() = 0;

        virtual FdhReturnCode get_cnt(std::vector<long> &fdb) = 0;
        virtual FdhReturnCode get_pos(std::vector<float> &fdb) = 0;
        virtual FdhReturnCode get_current(std::vector<float> &fdb) = 0;
        virtual FdhReturnCode get_velocity(std::vector<float> &fdb) = 0;

        virtual FdhReturnCode get_errorcode(std::vector<long> &fdb) = 0;
        virtual FdhReturnCode get_status(std::vector<uint8_t> &fdb) = 0;
        virtual FdhReturnCode clear_errorcode() = 0;

        virtual FdhReturnCode get_comm_config(std::string &cfg) = 0;
        virtual FdhReturnCode set_comm_config(std::string cfg) = 0;

        virtual FdhReturnCode get_pos_limited(std::vector<float> &fdb) = 0;
        virtual FdhReturnCode get_velocity_limited(std::vector<float> &fdb) = 0;
        virtual FdhReturnCode get_current_limited(std::vector<float> &fdb) = 0;

        virtual FdhReturnCode set_velocity_limited(uint8_t id, float max_speed) = 0;
        virtual FdhReturnCode set_pos_limited(uint8_t id, float start_angel, float end_angle) = 0;
        virtual FdhReturnCode set_current_limited(uint8_t id, float max_current) = 0;

        virtual FdhReturnCode set_pos(std::vector<float> _cmd) = 0;
        virtual FdhReturnCode set_velocity(std::vector<float> _cmd) = 0;
        virtual FdhReturnCode set_current(std::vector<float> _cmd) = 0;
#ifdef FDHX_TOOLS
        virtual FdhReturnCode set_pwm(std::vector<float> _cmd) = 0;
#endif
        virtual FdhReturnCode fast_set_positions(std::vector<float> pos) = 0;

        virtual FdhReturnCode get_ts_matrix(std::vector<std::vector<uint8_t>> &matrix) = 0;
        virtual FdhReturnCode get_ts_tashan(std::vector<std::vector<float>> &tashan) = 0;
        virtual FdhReturnCode get_ntc(int &temp) = 0;

        virtual FdhReturnCode get_pvc(std::vector<std::vector<float>> &fdb) = 0;
    };
}

#endif /* __BASEHAND_H__ */
