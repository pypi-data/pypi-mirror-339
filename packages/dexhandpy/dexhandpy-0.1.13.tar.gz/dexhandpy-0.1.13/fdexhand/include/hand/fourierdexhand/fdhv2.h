#ifndef __FDHV2_H__
#define __FDHV2_H__

#include <vector>
#include "basehand.h"

namespace BaseHandProtocol
{
    class Fdhv2 : public BaseHand
    {
    private:
        std::string ip_;

        // send msg list
        std::string get_matrix_com = "{\"method\":\"GET\",\"cmd\":\"/matrix\"}";
        std::string get_tashan_com = "{\"method\":\"GET\",\"cmd\":\"/tashan\"}";
        std::string get_pva_com = "{\"method\":\"GET\",\"cmd\":\"/pva\"}";

        std::string get_config_comm = "{\"method\":\"GET\",\"cmd\":\"/config\"}";
        std::string get_config_ctrl = "{\"method\":\"GET\",\"cmd\":\"/config\"}";

        std::string get_status_protocol = "{\"method\":\"GET\",\"cmd\":\"/errorcode\"}";

        std::string calibration_protocol = "{\"method\":\"SET\",\"cmd\":\"/calibration\"}";
        std::string disable_protocol = "{\"method\":\"SET\",\"cmd\":\"/disable\"}";
        std::string enable_protocol = "{\"method\":\"SET\",\"cmd\":\"/enable\"}";
        std::string set_pwm_protocol = "{\"method\":\"SET\",\"cmd\":\"/pwm\"}";
        std::string set_pos_protocol = "{\"method\":\"SET\",\"cmd\":\"/pos\"}";

    public:
        Fdhv2(std::string ip);
        ~Fdhv2();

        FdhReturnCode calibration() override;
        FdhReturnCode enable() override;
        FdhReturnCode disable() override;
        FdhReturnCode reboot() override;

        FdhReturnCode get_cnt(std::vector<long> &fdb) override;
        FdhReturnCode get_pos(std::vector<float> &fdb) override;
        FdhReturnCode get_current(std::vector<float> &fdb) override;
        FdhReturnCode get_velocity(std::vector<float> &fdb) override;

        FdhReturnCode get_errorcode(std::vector<long> &fdb) override;
        FdhReturnCode get_status(std::vector<uint8_t> &fdb) override;
        FdhReturnCode clear_errorcode() override;

        FdhReturnCode get_comm_config(std::string &cfg) override;
        FdhReturnCode set_comm_config(std::string cfg) override;

        FdhReturnCode get_pos_limited(std::vector<float> &fdb) override;
        FdhReturnCode get_velocity_limited(std::vector<float> &fdb) override;
        FdhReturnCode get_current_limited(std::vector<float> &fdb) override;

        FdhReturnCode set_velocity_limited(uint8_t id, float max_speed) override;
        FdhReturnCode set_pos_limited(uint8_t id, float start_angel, float end_angle) override;
        FdhReturnCode set_current_limited(uint8_t id, float max_current) override;

        FdhReturnCode set_pos(std::vector<float> _cmd) override;
        FdhReturnCode set_velocity(std::vector<float> _cmd) override;
        FdhReturnCode set_current(std::vector<float> _cmd) override;

#ifdef FDHX_TOOLS
        FdhReturnCode set_pwm(std::vector<float> _cmd) override;
#endif

        FdhReturnCode fast_set_positions(std::vector<float> pos) override;

        FdhReturnCode get_ts_matrix(std::vector<std::vector<uint8_t>> &matrix) override;
        FdhReturnCode get_ts_tashan(std::vector<std::vector<float>> &tashan) override;
        FdhReturnCode get_ntc(int &temp) override;

        FdhReturnCode get_pvc(std::vector<std::vector<float>> &fdb) override;
    };
}
#endif
