export function SimpleField({input, meta, label, placeholder, submitError}) {
  return <div>
    <label>{label}</label>
    <input {...input} placeholder={placeholder}/>
    {meta.error && meta.touched && <span>{meta.error}</span>}
    {submitError && <span>{submitError}</span>}
  </div>
}


export function SimpleSelect({input, meta, label, options, submitError}) {
  return <div>
    <label>{label}</label>
    <select  {...input}>
      {Object.keys(options).map(option => <option key={"select" + option} value={option}>
        {options[option]}
      </option>)}
    </select>
    {meta.error && meta.touched && <span>{meta.error}</span>}
    {submitError && <span>{submitError}</span>}
  </div>
}
