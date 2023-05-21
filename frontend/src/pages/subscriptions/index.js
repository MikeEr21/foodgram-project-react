import { Title, Pagination, Container, Main, SubscriptionList  } from '../../components'
import { useSubscriptions } from '../../utils'
import api from '../../api'
import { useEffect } from 'react'
import MetaTags from 'react-meta-tags'
import { useState } from 'react';

const SubscriptionsPage = () => {
  const {
    subscriptions,
    setSubscriptions,
    subscriptionsCount,
    setSubscriptionsCount,
    removeSubscription,
    subscriptionsPage,
    setSubscriptionsPage
  } = useSubscriptions()

  const [error, setError] = useState(null);

  const getSubscriptions = ({ page }) => {
    api
      .getSubscriptions({ page })
      .then(res => {
        setSubscriptions(res.results)
        setSubscriptionsCount(res.count)
      })
    .catch(error => {
        if (error.response && error.response.status === 400) {
          alert(error.response.data.errors);
        }
      });
  }

  useEffect(_ => {
    getSubscriptions({ page: subscriptionsPage })
  }, [subscriptionsPage])


  return <Main>

    <Container>
      {error && <div className="error-message">{error}</div>}
      <MetaTags>
        <title>Мои подписки</title>
        <meta name="description" content="Продуктовый помощник - Мои подписки" />
        <meta property="og:title" content="Мои подписки" />
      </MetaTags>
      <Title
        title='Мои подписки'
      />
      <SubscriptionList
        subscriptions={subscriptions}
        removeSubscription={removeSubscription}
      />
      <Pagination
        count={subscriptionsCount}
        limit={6}
        onPageChange={page => {
          setSubscriptionsPage(page)
        }}
      />
    </Container>
  </Main>
}

export default SubscriptionsPage