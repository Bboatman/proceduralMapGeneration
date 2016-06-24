#ifndef SCOPED_PTR_H_
#define SCOPED_PTR_H_

template<typename T>
class scoped_ptr {
 public:
  explicit scoped_ptr(T* p) : p_(p) { }
  ~scoped_ptr() { delete p_; }

  T* operator->() const { return p_; }

 private:
  T* p_;
};

#endif  // SCOPED_PTR_H_
