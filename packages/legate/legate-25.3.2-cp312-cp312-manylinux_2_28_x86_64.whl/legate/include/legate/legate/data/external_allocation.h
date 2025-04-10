/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2025 NVIDIA CORPORATION & AFFILIATES. All rights
 * reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include <legate/mapping/mapping.h>
#include <legate/utilities/detail/doxygen.h>
#include <legate/utilities/internal_shared_ptr.h>
#include <legate/utilities/shared_ptr.h>

#include <functional>
#include <optional>

/**
 * @file
 * @brief Class definition for legate::ExternalAllocation
 */

namespace legate::detail {

class ExternalAllocation;

}  // namespace legate::detail

namespace legate {

/**
 * @addtogroup data
 * @{
 */

/**
 * @brief Descriptor for external allocations
 *
 * An `ExternalAllocation` is a handle to a memory allocation outside Legate's memory management.
 * `ExternalAllocation` objects are used when users want to create Legate stores from the existing
 * allocations external to Legate. (See two overloads of `Runtime::create_store()` that
 * take `ExternalAllocation`s.)
 *
 * `ExternalAllocation`s can be tagged either read-only or mutable. In case of the latter, Legate
 * guarantees that any updates to the store to which the allocation is attached are also visible via
 * the allocation, wherever the updates are made, at the expense of block-waiting on tasks updating
 * the store. No such propagation of changes happens for read-only external allocations.
 *
 * The client code that creates an external allocation and attaches it to a Legate store must
 * guarantee that the allocation stays alive until all the tasks accessing the store are finished.
 * If the attached allocation was read-only, the code must not mutate the contents of the
 * allocation while the tasks are still running. An external allocation attached to a store can be
 * safely deallocated in two ways:
 *
 * 1) The client code calls the `detach()` method on the store before it dellocate the
 *    allocation. The `detach()` call makes sure that all outstanding operations on the store
 *    complete (see `LogicalStore::detach()`).
 * 2) The client code can optionally pass in a deleter for the allocation, which will be
 *    invoked once the store is destroyed and the allocation is no longer in use.
 *
 * Deleters don't need to be idempotent; Legate makes sure that they will be invoked only once
 * on the allocations. Deleters must not throw exceptions (throwable deleters are disallowed by
 * the type system). Deleters need not handle null pointers correctly, as external allocations
 * are not allowed to be created on null pointers. Each deleter is responsible for deallocating
 * only the allocation it is associated with and no other allocations.
 */
class ExternalAllocation {
 public:
  /**
   * @brief Signature for user-supplied deletion function.
   */
  using Deleter = std::function<void(void*)>;

  explicit ExternalAllocation(InternalSharedPtr<detail::ExternalAllocation>&& impl);

  /**
   * @brief Indicates if the allocation is read-only
   *
   * @return true If the allocation is read-only
   * @return false Otherwise
   */
  [[nodiscard]] bool read_only() const;

  /**
   * @brief Returns the kind of memory to which the allocation belongs
   *
   * @return Memory kind in a `mapping::StoreTarget`
   */
  [[nodiscard]] mapping::StoreTarget target() const;

  /**
   * @brief Returns the beginning address of the allocation
   *
   * @return Address to the allocation
   */
  [[nodiscard]] void* ptr() const;

  /**
   * @brief Returns the allocation size in bytes
   *
   * @return Allocation size in bytes
   */
  [[nodiscard]] std::size_t size() const;

  /**
   * @brief Creates an external allocation for a system memory
   *
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param read_only Indicates if the allocation is read-only
   * @param deleter Optional deleter for the passed allocation. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   */
  [[nodiscard]] static ExternalAllocation create_sysmem(
    void* ptr,
    std::size_t size,
    bool read_only                 = true,
    std::optional<Deleter> deleter = std::nullopt);

  /**
   * @brief Creates a read-only external allocation for a system memory
   *
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param deleter Optional deleter for the passed allocation. Passing a deleter means that the
   * ownership of the allocation is transferred to the Legate runtime. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   */
  [[nodiscard]] static ExternalAllocation create_sysmem(
    const void* ptr, std::size_t size, std::optional<Deleter> deleter = std::nullopt);

  /**
   * @brief Creates an external allocation for a zero-copy memory
   *
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param read_only Indicates if the allocation is read-only
   * @param deleter Optional deleter for the passed allocation. Passing a deleter means that the
   * ownership of the allocation is transferred to the Legate runtime. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   * @throw std::runtime_error If Legate is not configured with CUDA support enabled
   */
  [[nodiscard]] static ExternalAllocation create_zcmem(
    void* ptr,
    std::size_t size,
    bool read_only                 = true,
    std::optional<Deleter> deleter = std::nullopt);

  /**
   * @brief Creates a read-only external allocation for a zero-copy memory
   *
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param deleter Optional deleter for the passed allocation. Passing a deleter means that the
   * ownership of the allocation is transferred to the Legate runtime. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   * @throw std::runtime_error If Legate is not configured with CUDA support enabled
   */
  [[nodiscard]] static ExternalAllocation create_zcmem(
    const void* ptr, std::size_t size, std::optional<Deleter> deleter = std::nullopt);

  /**
   * @brief Creates an external allocation for a framebuffer memory
   *
   * @param local_device_id Local device ID
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param read_only Indicates if the allocation is read-only
   * @param deleter Optional deleter for the passed allocation. Passing a deleter means that the
   * ownership of the allocation is transferred to the Legate runtime. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   * @throw std::runtime_error If Legate is not configured with CUDA support enabled
   * @throw std::out_of_range If the local device ID is invalid
   */
  [[nodiscard]] static ExternalAllocation create_fbmem(
    std::uint32_t local_device_id,
    void* ptr,
    std::size_t size,
    bool read_only                 = true,
    std::optional<Deleter> deleter = std::nullopt);

  /**
   * @brief Creates a read-only external allocation for a framebuffer memory
   *
   * @param local_device_id Local device ID
   * @param ptr Pointer to the allocation
   * @param size Size of the allocation in bytes
   * @param deleter Optional deleter for the passed allocation. Passing a deleter means that the
   * ownership of the allocation is transferred to the Legate runtime. If none is given, the user is
   * responsible for the deallocation.
   *
   * @return An external allocation
   *
   * @throw std::invalid_argument If the `ptr` is null
   * @throw std::runtime_error If Legate is not configured with CUDA support enabled
   * @throw std::out_of_range If the local device ID is invalid
   */
  [[nodiscard]] static ExternalAllocation create_fbmem(
    std::uint32_t local_device_id,
    const void* ptr,
    std::size_t size,
    std::optional<Deleter> deleter = std::nullopt);

  [[nodiscard]] const SharedPtr<detail::ExternalAllocation>& impl() const;

  ExternalAllocation()                                               = default;
  ExternalAllocation(const ExternalAllocation& other)                = default;
  ExternalAllocation& operator=(const ExternalAllocation& other)     = default;
  ExternalAllocation(ExternalAllocation&& other) noexcept            = default;
  ExternalAllocation& operator=(ExternalAllocation&& other) noexcept = default;
  ~ExternalAllocation() noexcept;

 private:
  SharedPtr<detail::ExternalAllocation> impl_{};
};

/** @} */

}  // namespace legate

#include <legate/data/external_allocation.inl>
