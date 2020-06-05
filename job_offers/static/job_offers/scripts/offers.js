const filterOffersBtn = document.querySelector('.form__submit');
const technologiesInput = document.querySelector('.technologies__input');
const experienceSelect = document.querySelector('.experience__select');
const locationInput = document.querySelector('.location__input');
const b2bCheckbox = document.querySelector('.contracts__container input[name="b2b"]');
const uopCheckbox = document.querySelector('.contracts__container input[name="uop"]');
const salaryMinInput = document.querySelector('.salary__container input[name="fork_min"]');
const salaryMaxInput = document.querySelector('.salary__container input[name="fork_max"]');

const gatherUserInput = () => {
    return {
        technologies: technologiesInput.value.split(",").map(item => item.trim()),
        experience: experienceSelect.value,
        location: locationInput.value,
        b2b: b2bCheckbox.checked,
        uop: uopCheckbox.checked,
        salaryMin: salaryMinInput.value,
        salaryMax: salaryMaxInput.value,
    }
}

const createFilterUrl = filters => {
    let url = window.location.href;
    url += url.indexOf('?') === -1 ? '?' : '';

    filters.technologies ? url += `&technologies=${filters.technologies.join('+')}` : null;
    filters.experience ? url += `&experience=${filters.experience}` : null;
    filters.location ? url += `&location=${filters.location}` : null;
    filters.uop ? url += `&uop=true` : null;
    filters.b2b ? url += `&b2b=true` : null;
    filters.salaryMin ? url += `&fork_min=true` : null;
    filters.salaryMax ? url +=`&fork_max=true` : null;

    return url;
}

filterOffersBtn.addEventListener('click', e => {
    e.preventDefault();

    const filters = gatherUserInput();
    const url = createFilterUrl(filters);

    window.location.assign(url);
});
