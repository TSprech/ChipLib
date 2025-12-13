import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'From Datasheet',
    Svg: require('@site/static/img/datasheet_icon.svg').default,
    description: (
      <>
        Datasheets are great for conveying all the information about a chip, but not so great for creating libraries.
      </>
    ),
  },
  {
    title: 'To ChipLib',
    Svg: require('@site/static/img/yaml_icon.svg').default,
    description: (
      <>
        ChipLib specifies a language-agnostic format for describing the registers, fields, and enumerations for a chip.
      </>
    ),
  },
  {
    title: 'To Your Favorite Language',
    Svg: require('@site/static/img/generator_icon.svg').default,
    description: (
      <>
        Generate consistent, clear libraries in any language, according to any library format from the ChipLib file.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
