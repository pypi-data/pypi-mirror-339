/*******************************************************************************
 * Copyright 2019 Brainchip Holdings Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ********************************************************************************
 */

#pragma once

#include <cstdint>
#include <memory>
#include <vector>

#include "akida/hw_version.h"
#include "akida/ip_version.h"
#include "akida/np.h"
#include "infra/exports.h"

namespace akida {

class HardwareDevice;

class Device;

using DevicePtr = std::shared_ptr<Device>;
using DeviceConstPtr = std::shared_ptr<const Device>;

/**
 * class Device
 *
 * Public interface to an Akida Device (real or virtual)
 *
 */
class AKIDASHAREDLIB_EXPORT Device {
 public:
  virtual ~Device() = default;
  /**
   * @brief Get the Device version
   * @return a HwVersion
   */
  virtual HwVersion version() const = 0;

  /**
   * @brief Get the Device IP version
   * @return a IpVersion
   */
  IpVersion get_ip_version() const {
    return version().product_id == 0xA2 ? IpVersion::v2 : IpVersion::v1;
  }

  /**
   * @brief Get the Device description
   * @return a char*
   */
  virtual const char* desc() const = 0;

  /**
   * @brief Return the Device Neural Processor Mesh layout
   *
   * @return a reference to a np::Mesh structure
   */
  virtual const np::Mesh& mesh() const = 0;

  /**
   * @brief Return the Hardware Device if exist
   *
   * @return a pointer to a HardwareDevice
   */
  virtual HardwareDevice* hardware() const = 0;
};

}  // namespace akida
